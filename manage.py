#!/usr/bin/env python
import argparse
import http
import os
import subprocess
import time
from threading import Thread
from urllib.request import urlopen

from werkzeug.serving import run_simple

from pusto import build, create_app

ROOT_DIR = os.path.dirname(__file__)
SRC_DIR = ROOT_DIR + '/data'
BUILD_DIR = ROOT_DIR + '/build'
ssh = lambda cmd: subprocess.call(
    'ssh yadro.org "%s"' % cmd.replace('"', '\"').replace('$', '\$'),
    shell=True
)


def process_args(args=None):
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
        .arg('--no-reloader', action='store_true')\
        .exe(lambda a: run_simple(
            a.host, a.port, create_app(SRC_DIR, debug=True),
            use_reloader=not a.no_reloader, use_debugger=True,
            static_files={'': SRC_DIR}
        ))

    sub('build', help='build static content from `data` directory')\
        .arg('-s', '--serve', action='store_true', help='run static server')\
        .arg('--port', type=int, default=8000)

    sub('test_urls', help='test urls from google')\
        .arg('-w', '--use-wsgi', action='store_true', help='use wsgi server')\
        .exe(lambda a: check_urls(SRC_DIR, use_wsgi=a.use_wsgi))

    sub('deploy')

    args = parser.parse_args(args)
    if not hasattr(args, 'sub'):
        parser.print_usage()

    elif hasattr(args, 'exe'):
        args.exe(args)

    elif args.sub == 'build':
        build(SRC_DIR, BUILD_DIR)
        if args.serve:
            os.chdir(BUILD_DIR)
            http.server.test(
                http.server.SimpleHTTPRequestHandler, port=args.port
            )

    elif args.sub == 'deploy':
        ssh(
            'cd /home/pusto/src'
            '&& git pull'
            '&& source $(cat .venv)/bin/activate'
            '&& ./manage.py build'
            '&& systemctl restart nginx.service'
        )

    else:
        raise ValueError('Wrong subcommand')


def check_urls(src_dir, use_wsgi=False):
    if use_wsgi:
        args = 'run --port=9000 --no-reloader'.split(' ')
    else:
        args = 'build -s --port=9000'.split(' ')
    server = Thread(target=process_args, args=(args,))
    server.daemon = True
    server.start()
    time.sleep(2)

    urls = [
        # s.pusto.org/napokaz/
        # s.pusto.org/writing/ru-pycon-2013/
        '/resume',
        '/naspeh/detail/',
        '/naspeh/unikalnyy-nik/',
        '/naspeh/gnome-optimizaciya-okon/',
        '/naspeh/python-code-management/',
        '/naspeh/lakonichnost-testov-v-python/',
        '/post/avtozagruzka-klassov-v-prilozheniyah-na-zend-framework',
        (
            '/blog/2008/09/25/'
            'avtozagruzka-klassov-v-prilozheniyah-na-zend-framework/'
        )
    ]
    err = []
    for url in urls:
        res = urlopen('http://localhost:9000' + url)
        code = res.status
        expected_code = 200
        if code != expected_code:
            err += ['%s (%r != %r)' % (url, code, expected_code)]
    if err:
        print('Errors:')
        print('\n'.join(err))
    else:
        print('OK')


if __name__ == '__main__':
    process_args()
