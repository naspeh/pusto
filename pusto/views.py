from naya import Module


root = Module(__name__)


@root.route('/')
def index(app):
    return 'From index view'
