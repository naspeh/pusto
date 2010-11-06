from naya import App
from naya.ext.jinja import filters

from . import views


app = App(__name__, {
    'debug': True,
    'submodules': {
        '': views.mod,
    },
    'jinja': {
        'url_prefix': '/',
        'path_ends': ['.html', '/index.html'],
        'filters': filters.all
    }
})
