from naya.helpers import marker

from . import text


REDIRECTS = (
    ('/post/avtozagruzka-klassov-v-prilozheniyah-na-zend-framework/',
    'blog/2008/09/25/avtozagruzka-klassov-v-prilozheniyah-na-zend-framework',
    'r/zf-autoload'),
    ('/post/unikalniy-nick/', 'r/nick'),
)


@marker.defaults()
def defaults():
    return {
        'modules': {'text': text}
    }


@marker.route('/<path:path>')
def redirector(app, path):
    path = path.rstrip('/')
    for paths in REDIRECTS:
        if path in paths:
            return app.redirect(paths[0])
    app.abort(404)


@marker.with_login()
@marker.route('/login/')
def login(app):
    return app.redirect('/')


@marker.route('/logout/')
def logout(app):
    app.logout()
    return app.redirect('/')
