from jinja2 import DebugUndefined
from naya.base import Naya

from . import views, models
from .markup import markdown, rst
from .mongo import MongoMixin
from .openid import OpenidMixin


class App(Naya, MongoMixin, OpenidMixin):
    import_name = __name__

    @Naya.marker.config()
    def config(self):
        return {
            'debug': True,
            'modules': {'': views},
            'theme': {
                'url_prefix': '/',
            },
            'jinja': {
                'url_prefix': '/',
                'path_ends': ['/index.html', '.html'],
                'path_allow': [
                    '^(|naspeh|resume|post/[-\w]*)$',
                    '^_mockups\/',
                    '^_styles\/main\.css$',
                ],
                'env': {
                    'filters': {'rst': rst, 'markdown': markdown},
                    'options': {
                        'autoescape': False,
                        'trim_blocks': True,
                        'undefined': DebugUndefined
                    }
                }
            },
            'mongo': {
                'db': 'pusto',
                'models': [models]
            },
            'admin': 'naspeh'
        }
