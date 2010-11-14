from naya import App

from . import views
from .jinja import filters

app = App(__name__, {
    'debug': True,
    'modules': {
        '': views.mod,
    },
    'jinja': {
        'url_prefix': '/',
        'path_ends': ['/index.html', '.html'],
        'path_allow': ['index.html', 'naspeh.html', 'resume.html', 'post/*'],
        'filters': filters.all_by_name
    }
})
