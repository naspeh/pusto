from naya.helpers import marker

from . import auth, text, node


@marker.defaults()
def defaults():
    return {
        'modules': {
            'text': (text, {'prefix': ''}),
            'auth': (auth, {'prefix': ''}),
            'node': (node, {'prefix': ''})
        }
    }
