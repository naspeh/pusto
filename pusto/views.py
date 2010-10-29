from naya import Module


root = Module(__name__)


@root.route('/')
def index(app):
    return 'From index view'


@root.route('/t/<path:path>')
def tpl(app, path):
    template = app.jinja.get_template(path)
    return template.render(app=app)
