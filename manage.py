#!/usr/bin/env python
from naya.script import make_shell, sh
from werkzeug.script import make_runserver, run

from pusto import App


app = App()

sh.defaults(host='yadro.org', params={
    'activate': 'source .env/bin/activate && which python',
    'env_path': '.env',
    'sock_path': '/tmp/pusto-uwsgi.sock',
    'project_path': '/var/www/nanaya',
})


def action_pep8(target='.'):
    '''Run pep8.'''
    sh('pep8 --ignore=E202 %s' % target)


def action_clean(mask=''):
    '''Clean useless files.'''
    masks = [mask] if mask else ['*.pyc', '*.pyo', '*~', '*.orig']
    command = ('find . -name "%s" -exec rm -f {} +' % mask for mask in masks)
    sh('\n'.join(command))


def action_code():
    '''Check code style.'''
    action_clean()
    action_pep8()
    sh('git diff | grep -5 print')


def action_rmdb():
    '''Drop database.'''
    app.mongo.drop_database(app['mongo:db'])


def action_remote(target=''):
    '''Call remote command.'''
    if not target:
        print('Error. Target no define')
        return

    sh(
        ['cd $project_path', '$activate', target],
        params={'m': './manage.py'},
        remote=True
    )


def action_deploy(kill=True, pip=True):
    '''Deploy code on server.'''
    sh(('cd $project_path', 'pwd', 'git pull origin master'))

    if pip:
        sh((
            'cd $project_path', '$activate', 'pwd',
            'pip install -r docs/pip.stage.txt',
        ))

    if kill:
        pids = sh(
            "ps -ef | grep $sock_path | grep -v grep | awk '{print $$2}'",
            capture=True
        )
        if pids:
            sh('kill %s' % pids.replace('\n', ' '))
        else:
            print('no kill...')

    sh('screen -d -m uwsgi -s $sock_path -w stage:app -H $env_path')


def action_test(target='', base=False, rm=False, failed=('f', False),
                with_coverage=('c', False), cover_package=('p', 'pusto')):
    '''Run tests.'''
    if rm:
        sh('rm .noseids .coverage')

    if base:
        command = ['nosetests']
    else:
        command = ['nosetests -v --with-doctest']

    if failed:
        command.append('--failed')
    if with_coverage:
        command.append('--with-coverage --cover-tests')
        if cover_package:
            command.append('--cover-package=%s' % cover_package)

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
