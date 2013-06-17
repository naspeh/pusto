#!/usr/bin/env python
from argh import dispatch_commands
from werkzeug.serving import run_simple

from yadro import app


def run(host='localhost', port=5000):
    '''Start dev server'''
    run_simple(host, port, app, use_reloader=True, use_debugger=True)

if __name__ == '__main__':
    dispatch_commands([run])
