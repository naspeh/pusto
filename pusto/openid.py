from functools import wraps

from naya.helpers import marker

from .ext.openid import Openid


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

        user = self.session.get('user', None)
        if user:
            user = self.db.User.find_one(self.object_id(user))
        self.user = user or None
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
        user = self.db.User.find_one({'email': user_['email']})
        if not user:
            user = self.db.User()
            user.update({'email': user_['email'], 'username': user_['name']})
            user.save()

        self.session['user'] = user['_id']
