from naya.base import Module

from . import text


mod = Module(__name__, {
    'maps': [(text.map, 'text')]
})


REDIRECTS = (
    ('/post/avtozagruzka-klassov-v-prilozheniyah-na-zend-framework/',
    'blog/2008/09/25/avtozagruzka-klassov-v-prilozheniyah-na-zend-framework',
    'r/zf-autoload'),
    ('/post/unikalniy-nick/', 'r/nick'),
)


@mod.route('/<path:path>')
def redirector(app, path):
    path = path.rstrip('/')
    for paths in REDIRECTS:
        if path in paths:
            return app.redirect(paths[0])
    app.abort(404)


@mod.route('/login/')
def login(app):
    return app.with_login(lambda: app.redirect('/'))()


@mod.route('/logout/')
def logout(app):
    app.with_logout()
    return 'ok'
