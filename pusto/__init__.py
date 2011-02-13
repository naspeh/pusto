from jinja2 import DebugUndefined
from naya.base import Naya

from . import root, static, models
from .app import AppMixin
from .markup import markdown, rst
from .mongo import MongoMixin
from .openid import OpenidMixin
from .static import StaticMixin


class App(AppMixin, Naya, MongoMixin, OpenidMixin, StaticMixin):
    import_name = __name__

    @Naya.marker.config()
    def config(self):
        return {
            'debug': True,
            'profiler': False,
            'admins': ['naspeh', 'k.kostyuk'],
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
                    '^(resume|post\/[^_][-\w]*)$',
                    '^_mockups\/',
                    '\.(css|less|js)$',
                ],
                'env': {
                    'filters': {'rst': rst, 'markdown': markdown},
                    'options': {
                        'autoescape': True,
                        'trim_blocks': True,
                        'undefined': DebugUndefined,
                        'extensions': [
                            'jinja2.ext.with_', 'jinja2.ext.autoescape'
                        ]
                    },
                }
            },
            'mongo': {
                'db': 'pusto',
                'models': [models]
            },
            'google_analytics': 'UA-6254112-1'
        }
