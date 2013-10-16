#!/usr/bin/env python
import subprocess

import pusto

sh = lambda cmd: print(cmd) or subprocess.call(cmd, shell=True)
ssh = lambda cmd: sh(
    'ssh yadro.org "%s"'
    % cmd.replace('"', '\"').replace('$', '\$')
)


def process_args():
    parser = pusto.get_parser()
    sub = parser.sub

    sub('deploy', help='deploy to server')\
        .arg('-c', '--clear', action='store_true', help='clear virtualenv')\
        .arg('-t', '--target', default='origin/master', help='checkout it')\
        .exe(lambda a: ssh(
            'cd /home/pusto/src'
            '&& git fetch origin' +
            '&& git checkout {}'.format(a.target) +
            '&& source $(cat .venv)/bin/activate' +
            ('&& virtualenv --clear $(echo $VIRTUAL_ENV)' if a.clear else '') +
            '&& ./bootstrap'
            '&& ./pusto.py build -b build-tmp'
            '&& rm -rf build'
            '&& mv build-tmp build'
            '&& systemctl restart nginx.service'
        ))

    sub('wheels', help='prepare wheels')\
        .exe(lambda a: sh(
            'pip wheel -r requirements.txt -w wheels'
            '&& pip install --no-install -d wheels wheel'
        ))

    sub('napokaz', help='napokaz updater')\
        .arg('--push', action='store_true')\
        .arg('--init', action='store_true')\
        .exe(lambda a: sh(
            'git remote add napokaz git@github.com:naspeh/napokaz.git'
            if a.init else
            'git subtree %s -P data/s/napokaz/src napokaz master'
            % ('push' if a.push else 'pull --squash')
        ))

    pusto.process(parser=parser)


if __name__ == '__main__':
    process_args()
