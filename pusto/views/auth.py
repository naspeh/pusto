from naya.helpers import marker


@marker.authorized()
@marker.route('/login/')
def login(app):
    return 'Hello <b>%s</b>, <a href="/logout/">logout</a>' % app.user['name']


@marker.route('/logout/')
def logout(app):
    if not app.user:
        return app.abort(400)
    user = app.user
    app.logout()
    return 'Goodbye <b>%s</b> , <a href="/login/">login</a>' % user['name']
