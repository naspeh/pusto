#!/usr/bin/env python
from naya.script import sh
from opster import command, dispatch


sh.defaults(host='yadro.org', params={
    'activate': 'source .env/bin/activate && which python',
    'env_path': '.env',
    'sock_path': '/tmp/pusto-uwsgi.sock',
    'project_path': '/var/www/nanaya',
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


@command(usage='drop|dump|restore')
def db(target):
    '''Drop or dump or restore database'''
    targets = ('drop', 'dump', 'restore')
    if not target or target not in targets:
        print('Usage: ./manage.py %s' % '|'.join(targets))

    app = make_app()
    if target == 'drop':
        app.mongo.drop_database(app['mongo:db'])
    elif target == 'dump':
        sh('mongodump -d{0}'.format(app['mongo:db']))
    elif target == 'restore':
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
def deploy(no_pip=('p', False, 'don\'t update pip requirements')):
    '''Deploy code on server'''
    sh(('cd $project_path', 'pwd', 'git pull origin master'))

    if not no_pip:
        pip(target='stage')

    uwsgi(restart=True)


@command()
def pip(target='devel'):
    '''Update pip requirements on server'''
    sh((
        'cd $project_path', '$activate', 'pwd',
        'pip install -r etc/pip/%s.txt' % target,
    ))


@command()
def uwsgi(
    restart=('r', False, 'with restart'),
    kill=('k', False, 'with killing pids'),
    pids=('p', False, 'show pids')
):
    '''Manage uwsgi'''
    def get_pids(info=True):
        pids = sh('pgrep -f $sock_path', capture=True, no_exit=True)
        pids = pids and pids.replace('\n', ' ') or None
        if not info:
            return pids

        if pids:
            print('Pids: %s' % pids)
        else:
            print('WARNING. No pids...')

    if pids:
        get_pids()

    if kill or restart:
        pids = get_pids(False)
        if pids:
            sh('kill %s' % pids)
        else:
            print('no kill...')

    if restart:
        sh(
            'screen -d -m '
            'uwsgi -s $sock_path -w stage:app -H$env_path --uid=nobody -b 8192'
        )
        get_pids()


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
    hostname=('h', 'localhost', 'server name'),
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
