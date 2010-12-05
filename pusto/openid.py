"""
    Implementation of OpenId authentication scheme.

    Ported from `tipfy.ext.auth.openid`_.

    .. _`tipfy.ext.auth.openid`: http://code.google.com/p/tipfy-ext-auth-openid

    :copyright: 2009 Facebook.
    :copyright: 2010 tipfy.org.
    :license: Apache License Version 2.0, see LICENSE.txt for more details.
"""
import logging
import urllib
import urlparse
from functools import wraps

from naya.helpers import marker
from werkzeug import url_encode, Response, redirect


class OpenidMixin(object):
    @marker.defaults()
    def openid_defaults(self):
        return {'openid': {
            'endpoint': 'https://www.google.com/accounts/o8/ud',
            'ax_attrs': ['email'],
        }}

    @marker.wrap_handler()
    def openid_wrap_handler(self, handler):
        for mark in marker.with_login.get(handler):
            handler = self.with_login(handler)

        self.user = self.session.get('user', None)
        return handler

    def with_login(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            if 'user' in self.session:
                return func(*args, **kwargs)

            openid = Openid(
                self.request, self['openid:endpoint'], self['openid:ax_attrs']
            )
            if self.request.args.get('openid.mode', None):
                openid.get_user(self.openid_complete)
                return func(*args, **kwargs)
            return openid.redirect()
        return decorated

    def logout(self):
        self.user = None
        if 'user' in self.session:
            del self.session['user']

    def openid_complete(self, user):
        if not user:
            self.abort(403)
        self.session['user'] = user


class Openid(object):
    def __init__(self, request, openid_endpoint, ax_attrs=None):
        self.request = request
        self.openid_endpoint = openid_endpoint
        self.ax_attrs = ax_attrs or ('name', 'email', 'language', 'username')

    def redirect(self, callback_uri=None):
        """Returns the authentication URL for this service.

        After authentication, the service will redirect back to the given
        callback URI.
        """
        callback_uri = callback_uri or self.request.path
        args = self.args(callback_uri)
        return redirect(self.openid_endpoint + '?' + url_encode(args))

    def get_user(self, callback):
        """Fetches the authenticated user data upon redirect.

        :param callback:
            A function that is called after the authentication attempt. It
            is called passing a dictionary with the requested user attributes
            or ``None`` if the authentication failed.
        :return:
            The result from the callback function.
        """
        args = dict((k, v[-1]) for k, v in self.request.args.lists())
        args['openid.mode'] = u'check_authentication'
        url = self.openid_endpoint + '?' + url_encode(args)
        response = Response(urllib.urlopen(url))
        return self.verified(callback, response)

    def args(self, callback_uri, oauth_scope=None):
        """Builds and returns the OpenId arguments used in the authentication
        request.

        :param callback_uri:
            The URL to redirect to after authentication.
        :param oauth_scope:
        :return:
            A dictionary of arguments for the authentication URL.
        """
        url = urlparse.urljoin(self.request.url, callback_uri)
        args = {
            'openid.ns': 'http://specs.openid.net/auth/2.0',
            'openid.claimed_id':
                'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.identity':
                'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.return_to': url,
            'openid.realm': self.request.environ['wsgi.url_scheme'] + \
                '://' + self.request.host + '/',
            'openid.mode': 'checkid_setup',
        }
        if self.ax_attrs:
            args.update({
                'openid.ns.ax': 'http://openid.net/srv/ax/1.0',
                'openid.ax.mode': 'fetch_request',
            })
            ax_attrs = set(self.ax_attrs)
            required = []
            if 'name' in ax_attrs:
                ax_attrs -= set(['name', 'firstname', 'fullname', 'lastname'])
                required += ['firstname', 'fullname', 'lastname']
                args.update({
                    'openid.ax.type.firstname':
                        'http://axschema.org/namePerson/first',
                    'openid.ax.type.fullname':
                        'http://axschema.org/namePerson',
                    'openid.ax.type.lastname':
                        'http://axschema.org/namePerson/last',
                })

            known_attrs = {
                'email': 'http://axschema.org/contact/email',
                'language': 'http://axschema.org/pref/language',
                'username': 'http://axschema.org/namePerson/friendly',
            }

            for name in ax_attrs:
                args['openid.ax.type.' + name] = known_attrs[name]
                required.append(name)

            args['openid.ax.required'] = ','.join(required)

        if oauth_scope:
            args.update({
                'openid.ns.oauth':
                    'http://specs.openid.net/extensions/oauth/1.0',
                'openid.oauth.consumer': self.request.host.split(':')[0],
                'openid.oauth.scope': oauth_scope,
            })

        return args

    def verified(self, callback, response):
        """Called after the authentication attempt. It calls the callback
        function set when the authentication process started, passing a
        dictionary of user data if the authentication was successful or
        ``None`` if it failed.

        :param callback:
            A function that is called after the authentication attempt. It
            is called passing a dictionary with the requested user attributes
            or ``None`` if the authentication failed.
        :param response:
            The response returned from the urlfetch call after the
            authentication attempt.
        :return:
            The result from the callback function.
        """
        if not response:
            logging.warning('Missing OpenID response.')
            return callback(None)
        elif response.status_code < 200 or response.status_code >= 300:
            logging.warning('Invalid OpenID response (%d): %s',
                response.status_code, response.content)
            return callback(None)

        # Make sure we got back at least an email from Attribute Exchange.
        ax_ns = None
        for name, values in self.request.args.iterlists():
            if name.startswith('openid.ns.') and \
                values[-1] == u'http://openid.net/srv/ax/1.0':
                ax_ns = name[10:]
                break

        _ax_args = [
            ('email', 'http://axschema.org/contact/email'),
            ('name', 'http://axschema.org/namePerson'),
            ('first_name', 'http://axschema.org/namePerson/first'),
            ('last_name', 'http://axschema.org/namePerson/last'),
            ('username', 'http://axschema.org/namePerson/friendly'),
            ('locale', 'http://axschema.org/pref/language'),
        ]

        user = {}
        name_parts = []
        for name, uri in _ax_args:
            value = self.ax_arg(uri, ax_ns)
            if value:
                user[name] = value
                if name in ('first_name', 'last_name'):
                    name_parts.append(value)

        if not user.get('name'):
            if name_parts:
                user['name'] = u' '.join(name_parts)
            elif user.get('email'):
                user['name'] = user.get('email').split('@', 1)[0]

        return callback(user)

    def ax_arg(self, uri, ax_ns):
        """Returns an Attribute Exchange value from request.

        :param uri:
            Attribute Exchange URI.
        :param ax_ns:
            Attribute Exchange namespace.
        :return:
            The Attribute Exchange value, if found in request.
        """
        if not ax_ns:
            return u''

        prefix = 'openid.' + ax_ns + '.type.'
        ax_name = None
        for name, values in self.request.args.iterlists():
            if values[-1] == uri and name.startswith(prefix):
                part = name[len(prefix):]
                ax_name = 'openid.' + ax_ns + '.value.' + part
                break

        if not ax_name:
            return u''

        return self.request.args.get(ax_name, u'')
