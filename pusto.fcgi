#!/root/.virtualenvs/pusto/bin/python
from flup.server.fcgi import WSGIServer

from pusto import App


app = App(prefs={
    'debug': False,
})


WSGIServer(app, bindAddress='/tmp/pusto-fcgi.sock').run()
