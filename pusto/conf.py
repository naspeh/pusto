from . import views


def get_prefs(app):
    app.set_root(views.root)
    prefs = {'debug': True}
    return prefs
