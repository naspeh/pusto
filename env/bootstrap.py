#!/usr/bin/env python
from os.path import dirname, abspath
from subprocess import check_call

ROOT = dirname(dirname(abspath(__file__)))


def sh(cmd):
    print(cmd)
    return check_call(cmd, shell=True, cwd=ROOT)


def main():
    print('#### Install pip with wheels support...')
    sh('pip install -r env/req-wheels.txt')
    print('#### Install project dependencies from wheels...')
    sh('pip install -r env/req-dev.txt --no-index')

if __name__ == '__main__':
    main()
