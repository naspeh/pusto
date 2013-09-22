#!/usr/bin/env python
import argparse
import subprocess

sh = lambda cmd: print(cmd) or subprocess.call(cmd, shell=True)
ssh = lambda cmd: sh(
    'ssh yadro.org "%s"'
    % cmd.replace('"', '\"').replace('$', '\$')
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

    sub('bootstrap', help='install dependencies')\
        .exe(lambda a: sh('pip install -r requirements.txt --no-index'))

    sub('napokaz', help='napokaz updater')\
        .arg('--push', action='store_true')\
        .arg('--init', action='store_true')\
        .exe(lambda a: sh(
            'git remote add napokaz git@github.com:naspeh/napokaz.git'
            if a.init else
            'git subtree %s -P data/s/napokaz/src napokaz master'
            % ('push' if a.push else 'pull --squash')
        ))

    args = parser.parse_args(args)
    if not hasattr(args, 'sub'):
        parser.print_usage()
    else:
        args.exe(args)


if __name__ == '__main__':
    process_args()
