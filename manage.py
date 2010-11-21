#!/usr/bin/env python
from naya.script import make_shell, sh
from werkzeug.script import make_runserver, run

from pusto import app


sh.defaults(params={
    'activate': 'source /root/.virtualenvs/pusto/bin/activate && which python',
    'project_path': '/var/www/nanaya',
})


def action_pep8(target='.'):
    '''Run pep8.'''
    sh('pep8 --ignore=E202 %s' % target)


def action_clean(mask=''):
    '''Clean useless files.'''
    masks = [mask] if mask else ['*.pyc', '*.pyo', '*~', '*.orig']
    command = ('find . -name "%s" -exec rm -f {{}} +' % mask for mask in masks)
    sh('\n'.join(command))


def action_deploy(host='yadro.org', kill=True, server=('s', False)):
    '''Deploy code on server.'''
    if host and not server:
        sh(('pwd', 'git push origin master'))
        sh((
            '{activate}',
            'cd {project_path}', 'pwd',
            'git pull origin master',
            './manage.py deploy -s' + (not kill and ' --no-kill' or ''),
        ), host=host)
        return

    sh((
        '{activate}',
        'cd {project_path}', 'pwd', 'git pull origin master',
        'pip install -r docs/pip.stage.txt',
    ))

    if kill:
        sh(('killall pusto.fcgi'))

    sh((
        'screen -d -m {project_path}/pusto.fcgi',
    ))


def action_test(target='', clean=False, failed=('f', False),
                with_coverage=('c', False), cover_package=('p', 'pusto')):
    '''Run tests.'''
    if clean:
        command = ['nosetests']
    else:
        command = ['nosetests -v']

    if failed:
        command.append('--failed')
    if with_coverage:
        command.append('--with-coverage --cover-tests')
    if cover_package:
        command.append('--cover-package={0}'.format(cover_package))

    command.append('--with-id')

    if target:
        command.append(target)

    sh(' '.join(command))


action_shell = make_shell(lambda: {'app': app})
action_run = make_runserver(
    lambda: app, use_reloader=True, use_debugger=True
)


if __name__ == '__main__':
    run()
