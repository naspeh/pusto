from naya.helpers import marker


@marker.authorized()
@marker.route('/login/')
def login(app):
    return redirect(app)


@marker.route('/logout/')
def logout(app):
    app.logout()
    return redirect(app)


def redirect(app):
    to = '/'
    host_url = app.request.host_url.rstrip('/')
    deny = [
        host_url + app.url_for(':auth.login'),
        host_url + app.url_for(':auth.logout')
    ]
    headers = app.request.headers
    if 'Referer' in headers and headers['Referer'] not in deny:
        to = headers['Referer']
    return app.redirect(to)
