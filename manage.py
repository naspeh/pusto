#!/usr/bin/env python
import argparse
import http
import os
import re
import subprocess
import time
from threading import Thread
from urllib.request import urlopen
from urllib.error import HTTPError

from werkzeug.serving import run_simple

from pusto import build, create_app, watch_files

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
        .arg('--no-reloader', action='store_true')

    sub('build', help='build static content from `data` directory')\
        .arg('-b', '--bdir', default=BUILD_DIR, help='build directory')\
        .arg('-s', '--serve', action='store_true', help='run static server')\
        .arg('-n', '--nginx-file', help='write nginx rules')\
        .arg('--port', type=int, default=8000)

    sub('test_urls', help='test urls from google')\
        .arg('-w', '--use-wsgi', action='store_true', help='use wsgi server')\
        .arg('--host', help='use host for test')\
        .exe(lambda a: check_urls(SRC_DIR, use_wsgi=a.use_wsgi, host=a.host))

    sub('deploy').exe(lambda a: ssh(
        'cd /home/pusto/src'
        '&& git pull'
        '&& source $(cat .venv)/bin/activate'
        '&& ./manage.py build -b build-tmp'
        '&& rm -rf build'
        '&& mv build-tmp build'
        '&& systemctl restart nginx.service'
    ))

    args = parser.parse_args(args)
    if not hasattr(args, 'sub'):
        parser.print_usage()

    elif hasattr(args, 'exe'):
        args.exe(args)

    elif args.sub == 'run':
        touch_file = os.path.join(BUILD_DIR, '.nginx')
        if not args.no_reloader:
            with open(touch_file, 'w') as f:
                f.write('')
            watcher = Thread(target=watch_files, args=(SRC_DIR, touch_file))
            watcher.daemon = True
            watcher.start()

        run_simple(
            args.host, args.port, create_app(SRC_DIR, BUILD_DIR, debug=True),
            use_reloader=not args.no_reloader, use_debugger=True,
            static_files={'': BUILD_DIR}, extra_files=[touch_file]
        )
    elif args.sub == 'build':
        build(SRC_DIR, args.bdir, args.nginx_file)
        if args.serve:
            os.chdir(args.bdir)
            http.server.test(
                http.server.SimpleHTTPRequestHandler, port=args.port
            )

    else:
        raise ValueError('Wrong subcommand')


def check_urls(src_dir, use_wsgi=False, host=None):
    if not host:
        host = 'http://localhost:9000'
        if use_wsgi:
            args = 'run --port=9000 --no-reloader'.split(' ')
        else:
            args = 'build -s --port=9000'.split(' ')
        server = Thread(target=process_args, args=(args,))
        server.daemon = True
        server.start()
        time.sleep(2)

    urls = [
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
        ),
        '/yandex_5ad3ffab17496674.txt',
        '/googlee71e35f8e9cbd607.html',
        '/s/napokaz/',
        '/s/writing/ru-pycon-2013/',
    ]

    def get(url):
        comment = ''
        try:
            res = urlopen(host + url)
            text = res.read().decode()
            new = re.search(r'http-equiv="refresh" content="0;url=(.*)"', text)
            if new:
                new_url = new.groups(1)[0]
                res = urlopen(host + new_url)
                comment = 'Manual redirect'
            code = res.status
            res_url = res.url
        except HTTPError as e:
            code = e.code
            res_url = None
        return code, res_url, comment

    err = []
    for url in urls:
        code, res_url, comment = get(url)
        print('%s %s %s # %s' % (url, code, res_url, comment))
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
