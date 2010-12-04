from naya.base import App

from . import views, markup
from .mongo import MongoMixin
from .openid import OpenidMixin


class Pusto(App, MongoMixin, OpenidMixin):
    pass


app = Pusto(__name__, {
    'debug': True,
    'maps': [
        (views.mod, ''),
    ],
    'theme': {
        'url_prefix': '/',
    },
    'jinja': {
        'url_prefix': '/',
        'path_ends': ['/index.html', '.html'],
        'path_allow': [
            '^$', '^naspeh$', '^resume$', '^post/[-\w]*$',
            '^_mockups\/',
            '^_styles\/main\.css$',
        ],
        'filters': {'rst': markup.rst, 'markdown': markup.markdown}
    }
})
