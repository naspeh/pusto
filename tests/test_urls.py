from naya.testing import aye

from pusto import app
from pusto.views import REDIRECTS

c = app.test_client()


def test_allow_and_redirects():
    check('/', '/index.html')
    check('/resume/', '/resume.html')
    check('/naspeh/', '/naspeh.html')
    for item in REDIRECTS:
        check(*item)


def test_not_found():
    c.get('/not-found')


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
