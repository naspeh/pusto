from werkzeug.exceptions import abort
from werkzeug.wrappers import Request


@Request.application
def app(request):
    abort(404)
