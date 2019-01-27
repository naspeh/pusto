#!/usr/bin/env python
import logging
import subprocess

import pusto

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def sh(cmd):
    log.info(cmd)
    code = subprocess.call(cmd, shell=True)
    if code:
        raise SystemExit(code)
    return 0



def reqs(dev, clear, wheels):
    requirements = (
        'Jinja2 '
        'Pygments '
        'docutils '
        'lxml '
        'mistune '
        'pytz '
    )
    requirements += (
        'pytest '
        'ptpdb '
    ) if dev else ''

    sh('[ -d "$VIRTUAL_ENV" ] || (echo "ERROR: no virtualenv" && exit 1)')
    sh(
        (
            'rm -rf $VIRTUAL_ENV && virtualenv $VIRTUAL_ENV && '
            if clear else ''
        ) +
        'wheels="../wheels" &&'
        'pip install wheel && '
        'pip wheel -w $wheels -f $wheels {requirements} &&'
        'pip uninstall -y wheel &&'
        'pip install --no-index -f $wheels {requirements}'
        .format(requirements=requirements)
    )
    not dev and sh('pip freeze | sort > requirements.txt')


def process_args():
    parser, cmd = pusto.get_parser()

    cmd('rsync', help='rsync to server')\
        .exe(lambda a: sh(
            'rsync -av --delete ./build/ {0}:/opt/pusto/'
            '&& rsync -av ./deploy/nginx.conf {0}:/etc/nginx/conf.d/pusto.conf'
            '&& ssh {0} "nginx -s reload"'
            .format('root@h1.pusto.org')
        ))

    cmd('reqs', help='update python requirements')\
        .arg('-d', '--dev', action='store_true')\
        .arg('-c', '--clear', action='store_true')\
        .arg('-w', '--wheels', default='../wheels')\
        .exe(lambda a: reqs(a.dev, a.clear, a.wheels))

    cmd('docker', help='run docker container with nginx')\
        .exe(lambda a: sh(
            'docker run'
            '   -d -v $(pwd):/var/www -p 80:80 --name=pusto'
            '   pusto /bin/nginx'
        ))

    cmd('napokaz', help='napokaz updater')\
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
