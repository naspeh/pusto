#!/usr/bin/env python
from naya.script import sh
from opster import command, dispatch


sh.defaults(host='yadro.org', params={
    'activate': 'source ../env/bin/activate && which python',
    'env_path': '../env',
    'project_path': '/home/free/pusto/src',
})


def make_app():
    from pusto import App

    return App()


@command()
def clean(mask=None):
    '''Clean useless files'''
    masks = [mask] if mask else ['*.pyc', '*.pyo', '*~', '*.orig']
    command = ('find . -name "%s" -exec rm -f {} +' % mask for mask in masks)
    sh('\n'.join(command))


@command()
def code(target='.'):
    '''Check code style'''
    sh('pep8 --ignore=E202 %s' % target, no_exit=True)
    sh('pyflakes %s' % target, no_exit=True)
    sh('git diff | grep -1 print', no_exit=True)


@command()
def db_drop():
    '''Drop database'''
    app = make_app()
    app.mongo.drop_database(app['mongo:db'])


@command()
def db_dump(commit=('c', False, 'commit changes')):
    '''Dump database'''
    app = make_app()
    sh('mongodump -d{0}'.format(app['mongo:db']))
    if commit:
        sh([
            'git checkout dump/pusto/users.bson',
            'git add dump/',
            'git commit -m "Updated dump;"',
            'git push origin HEAD'
        ])


@command()
def db_restore():
    '''Restore database'''
    app = make_app()
    sh('mongorestore -d{0} dump/{0}'.format(app['mongo:db']))


@command()
def remote(target):
    '''Call remote command'''
    sh(
        ['cd $project_path', '$activate', target],
        params={'m': './manage.py'},
        remote=True
    )


@command()
def deploy(with_pip=('p', False, 'update pip requirements')):
    '''Deploy code on server'''
    sh(('cd $project_path', 'pwd', 'git pull origin master'))

    if with_pip:
        pip(target='stage')

    sh('touch ../reload')


@command()
def pip(target='devel'):
    '''Update pip requirements on server'''
    sh((
        'cd $project_path', '$activate', 'pwd',
        'pip install -r etc/pip/%s.txt' % target,
    ))


@command()
def test(
    target='',
    base=('', False, 'base nosetests command'),
    rm=('', False, 'remove pilot files'),
    failed=('f', False, 'with --failed option'),
    with_coverage=('c', False, 'with coverage options'),
    cover_package=('p', 'pusto', 'set coverage package')
):
    '''Run tests'''
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


@command()
def shell(no_bpython=('', False, 'don\'t use bpython')):
    '''Start a new interactive python session'''
    namespace = {'app': make_app()}
    banner = 'Interactive shell for `pusto`'
    if not no_bpython:
        try:
            import bpython
        except ImportError:
            pass
        else:
            bpython.embed(locals_=namespace, banner=banner)
            return

    from code import interact
    interact(banner, local=namespace)


@command()
def run(
    hostname=('n', 'localhost', 'server name'),
    port=('p', 5000, 'server port'),
    no_reloader=('', False, 'don\'t use reloader'),
    no_debugger=('', False, 'don\'t use debugger')
):
    '''Start a new development server'''
    from werkzeug.serving import run_simple
    app = make_app()
    run_simple(hostname, port, app, not no_reloader, not no_debugger)


if __name__ == '__main__':
    dispatch()
