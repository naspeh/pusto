from naya.base import Naya

from . import views, markup
from .mongo import MongoMixin
from .openid import OpenidMixin


class Pusto(Naya, MongoMixin, OpenidMixin):
    pass


app = Pusto(__name__, {
    'debug': True,
    'modules': {'': views},
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
        'env': {
            'filters': {'rst': markup.rst, 'markdown': markup.markdown}
        }
    }
})
