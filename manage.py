#!/usr/bin/env python
from fabric.api import local
from naya.script import make_shell
from werkzeug.script import make_runserver, run

from pusto import app


def action_pep8(target='.'):
    '''Run pep8.'''
    local('pep8 --ignore=E202 %s' % target, capture=False)


def action_clean(mask=''):
    '''Clean useless files.'''
    masks = [mask] if mask else ['*.pyc', '*.pyo', '*~', '*.orig']
    command = ('find . -name "%s" -exec rm -f {} +' % mask for mask in masks)
    local('\n'.join(command), capture=False)


action_shell = make_shell(lambda:{'app': app})
action_runserver = make_runserver(
    lambda: app, use_reloader=True, use_debugger=True
)


if __name__ == '__main__':
    run()
