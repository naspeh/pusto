from naya import App

from . import conf, views


app = App(views.root, conf.get_prefs)
