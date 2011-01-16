#!/root/.virtualenvs/pusto/bin/python
from flup.server.fcgi import WSGIServer

from stage import app


WSGIServer(app, bindAddress='/tmp/pusto-fcgi.sock').run()
