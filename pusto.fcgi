#!/usr/bin/python
import site
site.addsitedir('/root/.virtualenvs/pusto/lib/python2.6/site-packages')


def run():
    from flup.server.fcgi import WSGIServer
    from pusto import app

    WSGIServer(app, bindAddress='/tmp/pusto-fcgi.sock').run()

run()
