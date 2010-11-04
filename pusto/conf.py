from naya.ext.jinja import filters

from . import views


def get_prefs():
    return {
        'debug': True,
        'modules': {
            '': views.mod,
        },
        'jinja': {
            'url_prefix': '/',
            'path_ends': ['.html', '/index.html'],
            'filters': filters.all
        }
    }
