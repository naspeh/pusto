from jinja2 import DebugUndefined
from naya.base import Naya

from . import root, static, models
from .app import AppMixin
from .markup import markdown, rst
from .mongo import MongoMixin
from .openid import OpenidMixin


class App(Naya, AppMixin, MongoMixin, OpenidMixin):
    import_name = __name__

    @Naya.marker.config()
    def config(self):
        return {
            'debug': True,
            'modules': {
                '': root,
                'static': (static, {'prefix': ''}),
            },
            'theme': {
                'url_prefix': '/',
            },
            'jinja': {
                'url_prefix': '/',
                'path_ends': ['/index.html', '.html', '.rst'],
                'path_allow': [
                    '^(|naspeh|resume|post/[-\w]*)$',
                    '^_mockups\/',
                    '\.(css|less|js)$',
                ],
                'env': {
                    'filters': {'rst': rst, 'markdown': markdown},
                    'options': {
                        'autoescape': False,
                        'trim_blocks': True,
                        'undefined': DebugUndefined,
                        'extensions': ['jinja2.ext.with_']
                    },
                }
            },
            'mongo': {
                'db': 'pusto',
                'models': [models]
            },
            'admin': 'naspeh'
        }
