from naya.testing import aye, raises
from nose import with_setup

from . import app, client as c, authorize


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
    aye('==', app.url_for(':home'), c.path)
    aye(True, app.user)
    aye('in', app.user['name'], c.data)
    aye('in', app.url_for(':auth.logout'), c.data)


@with_setup(clean_auth)
def test_bad_session():
    app.session['user'] = {'name': 'naspeh'}
    c.get(app.url_for(':auth.login'), code=302)
    aye(False, app.user)


@with_setup(clean_auth)
def test_logout():
    test_login()

    c.get(app.url_for(':auth.logout'), code=200, follow_redirects=True)
    aye('==', app.url_for(':home'), c.path)
    aye('in', app.url_for(':auth.login'), c.data)
    aye('not in', 'user', app.session)
    aye(False, app.user)


def test_logout_with_referer():
    def logout(referer):
        test_login()
        referer = app.request.host_url.rstrip('/') + referer
        c.get(app.url_for(':auth.logout'),
            code=200, follow_redirects=True,
            headers=[('Referer', referer)]
        )

    referer = app.url_for(':text.edit')
    logout(referer)
    aye('==', referer, c.path)

    logout(app.url_for(':auth.logout'))
    aye('==', app.url_for(':home'), c.path)

    logout(app.url_for(':auth.login'))
    aye('==', app.url_for(':home'), c.path)
