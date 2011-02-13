from naya.helpers import marker

from . import auth, text, node


HOME_URL = '/naspeh/'


@marker.defaults()
def defaults():
    return {
        'modules': {
            'text': (text, {'prefix': ''}),
            'auth': (auth, {'prefix': ''}),
            'node': (node, {'prefix': ''})
        }
    }


@marker.route(HOME_URL)
@marker.route('/', redirect_to=HOME_URL)
def home(app):
    return node.show(app, HOME_URL.strip('/'))
