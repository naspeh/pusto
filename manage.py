#!/usr/bin/env python
import argparse
import os

from pusto import run_server, data

ROOT_DIR = os.path.dirname(__file__)
SRC_DIR = ROOT_DIR + '/data'
BUILD_DIR = ROOT_DIR + '/var/data'


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

    sub('build', help='build static content from `data` directory')

    args = parser.parse_args()
    if not hasattr(args, 'sub'):
        parser.print_usage()

    elif args.sub == 'run':
        run_server(args.host, args.port, SRC_DIR)

    elif args.sub == 'build':
        data.build(SRC_DIR, BUILD_DIR)


if __name__ == '__main__':
    process_args()
