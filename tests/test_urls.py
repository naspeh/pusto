from naya.testing import aye

from . import app
from pusto.static import REDIRECTS


c = app.test_client()


def test_allow_and_redirects():
    check('/')
    check('/resume/')
    check('/naspeh/')
    c.get('/googlee71e35f8e9cbd607.html/', code=302)
    c.get(c.path, code=200, follow_redirects=True)
    aye('==', c.path, '/googlee71e35f8e9cbd607.html')
    c.get(c.path, code=200)

    for item in REDIRECTS:
        check(*item)


def test_not_found():
    c.get('/not-found', code=404)


def check(main_url, *children):
    if isinstance(children, tuple):
        children = list(children)

    for url in list(children):
        without_slash = url.rstrip('/')
        with_slash = '%s/' % without_slash
        if not without_slash in children:
            children.append(without_slash)
        if not with_slash in children:
            children.append(with_slash)

    without_slash = main_url.rstrip('/')
    if without_slash and not without_slash in children:
        children.append(without_slash)

    for url in children:
        c.get(url, code=302)
        c.get(url, code=200, follow_redirects=True)
        aye('==', c.path, main_url)
