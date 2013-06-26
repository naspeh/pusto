#!/usr/bin/env python
import os
from http import server

from argh import arg, dispatch_commands
from werkzeug.serving import run_simple

from pusto import app, data


def run(host='localhost', port=5000):
    '''start dev server'''
    run_simple(host, port, app, use_reloader=True, use_debugger=True)


@arg('--serve', '-s', help='run server on `build` directory')
def build(serve=False):
    '''build static content from `data` directory'''
    build_dir = './var/data'
    data.build('./data', build_dir)
    if serve:
        os.chdir(build_dir)
        server.test(HandlerClass=server.SimpleHTTPRequestHandler)


if __name__ == '__main__':
    dispatch_commands([run, build])
