from naya import App as BaseApp

from . import views
from .jinja import filters
from .mongo import MongoMixin


class App(BaseApp, MongoMixin):
    pass


app = App(__name__, {
    'debug': True,
    'maps': [
        (views.mod, ''),
    ],
    'jinja': {
        'url_prefix': '/',
        'path_ends': ['/index.html', '.html'],
        'path_allow': [
            'index.html', 'naspeh.html', 'resume.html', 'post/*',
            'googlee71e35f8e9cbd607.html',
            '_mockups/*',
            #'*.*'
        ],
        'filters': filters.all_by_name
    }
})
