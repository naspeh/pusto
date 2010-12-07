from naya.helpers import marker


@marker.with_login()
@marker.route('/login/')
def login(app):
    return app.redirect('/')


@marker.route('/logout/')
def logout(app):
    app.logout()
    return app.redirect('/')
