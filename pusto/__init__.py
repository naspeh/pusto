from naya import App

from . import views
from .jinja import filters

app = App(__name__, {
    'debug': True,
    'submodules': {
        '': views.mod,
    },
    'jinja': {
        'url_prefix': '/',
        'path_ends': ['.html', '/index.html'],
        'filters': filters.all_by_name
    }
})
