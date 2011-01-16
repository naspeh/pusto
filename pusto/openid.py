from functools import wraps

from naya.helpers import marker

from .ext.openid import Openid


class OpenidMixin(object):
    @marker.defaults()
    def openid_defaults(self):
        return {
            'openid': {
                'endpoint': 'https://www.google.com/accounts/o8/ud',
                'ax_attrs': ['email'],
            },
            'admins': []
        }

    @marker.wrap_handler()
    def openid_wrap_handler(self, handler):
        for mark in marker.authorized.get(handler):
            handler = self.authorized(
                handler, *mark['args'], **mark['kwargs']
            )

        user = self.session.get('user', None)
        user = isinstance(user, basestring) and user or None
        if user:
            user = self.db.User.by_id(user)
        self.user = user or None
        return handler

    def authorized(self, func, as_admin=False):
        @wraps(func)
        def decorated(*args, **kwargs):
            if 'user' in self.session and self.user:
                if as_admin and not self.is_admin():
                    return self.abort(403)
                return func(*args, **kwargs)

            openid = Openid(
                self.request, self['openid:endpoint'], self['openid:ax_attrs']
            )
            if self.request.args.get('openid.mode', None):
                openid.get_user(self.openid_complete)
                return self.redirect(self.request.path)
            return openid.redirect()
        return decorated

    def logout(self):
        self.user = None
        if 'user' in self.session:
            del self.session['user']

    def openid_complete(self, user_):
        if not user_:
            self.abort(403)
        user = self.db.User.one({'email': user_['email']})
        if not user:
            user = self.db.User()
            user.update(user_)
            user.save()

        self.session['user'] = str(user['_id'])

    def is_admin(self, user=None):
        if not user:
            user = self.user
        return user and user['name'] in self['admins'] or False
