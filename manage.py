#!/usr/bin/env python
from naya.script import make_shell, sh
from werkzeug.script import make_runserver, run

from pusto import app


SERVER_PARAMS = {
    'activate': 'source /root/.virtualenvs/pusto/bin/activate && which python',
    'project_path': '/var/www/nanaya',
}


def action_pep8(target='.'):
    '''Run pep8.'''
    sh('pep8 --ignore=E202 %s' % target)


def action_clean(mask=''):
    '''Clean useless files.'''
    masks = [mask] if mask else ['*.pyc', '*.pyo', '*~', '*.orig']
    command = ('find . -name "%s" -exec rm -f {} +' % mask for mask in masks)
    sh('\n'.join(command))


def action_deploy(host='yadro.org', killall=True):
    '''Deploy code on server.'''
    if host:
        sh(('pwd', 'hg push'))
        sh((
            '{activate}',
            'cd {project_path}', 'pwd',
            'hg pull', 'hg up',
            './manage.py deploy ""' + (not killall and ' --no-killall' or ''),
        ), host=host, params=SERVER_PARAMS)
        return

    sh((
        '{activate}',
        'cd {project_path}', 'pwd', 'hg pull', 'hg up',
    ), params=SERVER_PARAMS)

    if killall:
        sh(('killall pusto.fcgi'))

    sh((
        'screen -d -m {project_path}/pusto.fcgi > /dev/null',
    ), params=SERVER_PARAMS)


action_shell = make_shell(lambda: {'app': app})
action_run = make_runserver(
    lambda: app, use_reloader=True, use_debugger=True
)


if __name__ == '__main__':
    run()
