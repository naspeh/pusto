#!/usr/bin/env python
import argparse
import http
import os

from werkzeug.serving import run_simple
from werkzeug.test import Client
from werkzeug.wrappers import Response

from pusto import build, create_app

ROOT_DIR = os.path.dirname(__file__)
SRC_DIR = ROOT_DIR + '/data'
BUILD_DIR = ROOT_DIR + '/build'


def process_args():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(title='subcommands')

    def sub(name, **kw):
        s = subs.add_parser(name, **kw)
        s.set_defaults(sub=name)
        s.arg = lambda *a, **kw: s.add_argument(*a, **kw) and s
        s.exe = lambda f: s.set_defaults(exe=f) and s
        return s

    sub('run', help='start dev server')\
        .arg('--host', default='localhost')\
        .arg('--port', type=int, default=5000)\
        .exe(lambda a: run_simple(
            a.host, a.port, create_app(SRC_DIR, debug=True),
            use_reloader=True, use_debugger=True,
            static_files={'': SRC_DIR}
        ))

    sub('build', help='build static content from `data` directory')\
        .arg('-s', '--serve', action='store_true', help='run static server')

    sub('test_urls', help='test urls from google')\
        .exe(lambda a: check_urls(SRC_DIR))

    args = parser.parse_args()
    if not hasattr(args, 'sub'):
        parser.print_usage()

    elif hasattr(args, 'exe'):
        args.exe(args)

    elif args.sub == 'build':
        build(SRC_DIR, BUILD_DIR)
        if args.serve:
            os.chdir(BUILD_DIR)
            http.server.test(HandlerClass=http.server.SimpleHTTPRequestHandler)
    else:
        raise ValueError('Wrong subcommand')


def check_urls(src_dir):
    app = create_app(src_dir)
    c = Client(app, Response)
    urls = [
        # s.pusto.org/napokaz/
        # s.pusto.org/writing/ru-pycon-2013/
        ('/resume', 302),
        ('/naspeh/detail/', 302),
        ('/naspeh/unikalnyy-nik/', 302),
        ('/naspeh/gnome-optimizaciya-okon/', 302),
        ('/naspeh/python-code-management/', 302),
        ('/naspeh/lakonichnost-testov-v-python/', 302),
        ('/post/avtozagruzka-klassov-v-prilozheniyah-na-zend-framework', 302),
        ('/blog/2008/09/25/'
            'avtozagruzka-klassov-v-prilozheniyah-na-zend-framework/', 302)
    ]
    err = []
    for url, expected_code in urls:
        code = c.get(url).status_code
        if code != expected_code:
            err += ['%s (%r != %r)' % (url, code, expected_code)]
    if err:
        print('Errors:')
        print('\n'.join(err))
    else:
        print('OK')


if __name__ == '__main__':
    process_args()
