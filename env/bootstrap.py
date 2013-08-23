#!/usr/bin/env python
from os.path import dirname, abspath
from subprocess import check_call

import pip

ROOT = dirname(dirname(abspath(__file__)))


def sh(cmd):
    print(cmd)
    return check_call(cmd, shell=True, cwd=ROOT)


def main():
    if not pip.__version__.startswith('1.4.'):
        raise SystemExit('Required `pip` with wheels support (pip >= 1.4)')

    print('#### Install project dependencies from wheels...')
    sh('pip install -r requirements.txt --no-index')

if __name__ == '__main__':
    main()
