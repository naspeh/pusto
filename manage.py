#!/usr/bin/env python
import argparse
import http
import os

from werkzeug.serving import run_simple

from pusto import app, data


def process_args():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers()

    def sub(name, **kw):
        s = subs.add_parser(name, **kw)
        s.set_defaults(sub=name)
        s.arg = lambda *a, **kw: s.add_argument(*a, **kw) and s
        return s

    sub('run', help='start dev server')\
        .arg('--host', default='localhost')\
        .arg('--port', type=int, default=5000)

    sub('build', help='build static content from `data` directory')\
        .arg('-s', '--serve', action='store_true', help='run server')

    args = parser.parse_args()
    if not hasattr(args, 'sub'):
        parser.print_usage()

    elif args.sub == 'run':
        run_simple(
            args.host, args.port, app,
            use_reloader=True, use_debugger=True
        )

    elif args.sub == 'build':
        build_dir = './var/data'
        data.build('./data', build_dir)
        if args.serve:
            os.chdir(build_dir)
            http.server.test(HandlerClass=http.server.SimpleHTTPRequestHandler)


if __name__ == '__main__':
    process_args()
