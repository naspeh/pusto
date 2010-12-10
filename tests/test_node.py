from naya.testing import aye

from . import app, clear_db, authorize
from pusto.ext.translit import slugify


c = app.test_client()
Node = app.db.Node


def setup():
    authorize(app['admin'])


def add_node(title='test title', code=302):
    title = unicode(title)
    code = 200 if not title else code
    c.post(app.url_for(':node.edit'), data={
        'parent': '',
        'title': title,
        'slug': '',
        'content': '',
    }, code=code)

    if not title:
        aye('in', 'slug is required', c.data)
        aye('in', 'title is required', c.data)
    else:
        node = Node.fetch_one({'slug': slugify(title)})
        aye(True, node)
        return node


def test_node_new():
    clear_db([Node])

    add_node('')
    node = add_node()
    aye(True, node['_id'])

    add_node(code=200)
    aye('in', 'duplicate key error index', c.data)


def test_fails():
    clear_db([Node])

    c.post(app.url_for(':node.edit'), data={'title': ''}, code=400)

    node = add_node()
    node.delete()
    c.get(app.url_for(':node.edit', id=node['_id']))
