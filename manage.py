#!/usr/bin/env python
import argparse
import json
import subprocess
import time
from http.client import HTTPConnection
from threading import Thread
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

    sub('test_urls', help='test url responses')\
        .arg('-v', '--verbose', action='store_true')\
        .arg('--host', help='use host for test')\
        .exe(lambda a: check_urls(host=a.host, verbose=a.verbose))

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


def check_urls(host=None, verbose=False):
    log = lambda *a: verbose and print(*a)

    if not host:
        pusto.process('build')
        host = 'localhost:9000'
        args = 'run --port=9000 --no-reloader'.split(' ')
        server = Thread(target=pusto.process, args=args)
        server.daemon = True
        server.start()
        time.sleep(2)

    with open('data/urls.json', 'br') as f:
        urls = json.loads(f.read().decode())

    def get(url, expected_code=200, indent=''):
        comment = ''
        try:
            conn = HTTPConnection(host)
            conn.request('HEAD', url)
            res = conn.getresponse()
            code = res.status
            if code == 200:
                res_url = url
            else:
                res_url = res.info().get('Location', '')
                res_url = res_url.replace('http://' + host, '')
        except HTTPError as e:
            code = e.code
            res_url = None

        err = []
        if code != expected_code:
            err = ['%s (%r != %r)' % (url, code, expected_code)]
        else:
            log('%s%s %s %s # %s' % (indent, url, code, res_url, comment))
        return err

    err = []
    for url in sorted(urls.keys()):
        aliases = urls.get(url)
        err += get(url)
        for alias in aliases or []:
            err += get(alias, expected_code=301, indent='  ')
    if err:
        print('Errors:')
        print('\n'.join(err))
    else:
        print('OK')


if __name__ == '__main__':
    process_args()
