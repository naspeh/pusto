from werkzeug.wrappers import Request, Response


@Request.application
def app(request):
    return Response('Hello Grisha!')
