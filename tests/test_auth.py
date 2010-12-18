from naya.testing import aye, raises
from nose import with_setup

from . import app, authorize


c = app.test_client()


def clean_auth():
    authorize()
    del app.session['user']
    app.user = None


@with_setup(clean_auth)
def test_login():
    login = app.url_for(':auth.login')
    raises(RuntimeError, lambda: c.get(login, code=200, follow_redirects=True))
    aye('not in', 'user', app.session)
    aye(False, app.user)

    name = u'naya'
    authorize(name)
    user = app.db.User.one({'name': name})

    aye(True, user)
    aye('in', 'user', app.session)
    aye('==', app.session['user'], str(user['_id']))

    c.get(login, code=200, follow_redirects=True)
    aye(True, app.user)
    aye('==', c.path, '/')


@with_setup(clean_auth)
def test_bad_session():
    app.session['user'] = {'name': 'naspeh'}
    c.get(app.url_for(':auth.login'), code=302)
    aye(False, app.user)


@with_setup(clean_auth)
def test_logout():
    test_login()

    c.get(app.url_for(':auth.logout'), code=200, follow_redirects=True)
    aye('==', c.path, '/')
    aye('not in', 'user', app.session)
    aye(False, app.user)
