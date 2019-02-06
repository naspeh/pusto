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



def process_args():
    parser, cmd = pusto.get_parser()

    cmd('rsync', help='rsync to server')\
        .exe(lambda a: sh(
            'rsync -av --delete ./build/ {0}:/opt/pusto/'
            '&& rsync -av ./deploy/nginx.conf {0}:/etc/nginx/conf.d/pusto.conf'
            '&& ssh {0} "nginx -s reload"'
            .format('root@h1.pusto.org')
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
