#!/usr/bin/env python
import argparse
import re
import subprocess
import time
from threading import Thread
from urllib.request import urlopen
from urllib.error import HTTPError

import pusto

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

    sub('test_urls', help='test urls from google')\
        .arg('--host', help='use host for test')\
        .exe(lambda a: check_urls(host=a.host))

    sub('deploy', help='deploy to server')\
        .exe(lambda a: ssh(
            'cd /home/pusto/src'
            '&& git pull'
            '&& source $(cat .venv)/bin/activate'
            '&& ./pusto.py build -b build-tmp'
            '&& rm -rf build'
            '&& mv build-tmp build'
            '&& systemctl restart nginx.service'
        ))

    args = parser.parse_args(args)
    if not hasattr(args, 'sub'):
        parser.print_usage()
    else:
        args.exe(args)


def check_urls(host=None):
    if not host:
        pusto.process('build')
        host = 'http://localhost:9000'
        args = 'run --port=9000 --no-reloader'.split(' ')
        server = Thread(target=pusto.process, args=args)
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
