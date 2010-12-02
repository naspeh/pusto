from naya.base import App as BaseApp

from . import views, markup
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
            '^$', '^naspeh$', '^resume$', '^post/[-\w]*$',
            '^googlee71e35f8e9cbd607\.html$',
            '^_mockups\/',
            '^_styles\/',
        ],
        'filters': {'rst': markup.rst, 'markdown': markup.markdown}
    }
})
