# -*- coding: utf-8 -*-
from naya.testing import aye

from . import app, clear_db, authorize, test_text
from pusto.ext.translit import slugify


c = app.test_client()
Node = app.db.Node


def setup():
    authorize(app['admin'])


def add_node(title='test title', parent=None, content=None):
    title = unicode(title)
    c.post(app.url_for(':node.edit'), data={
        'parent': parent or '',
        'title': title,
        'slug': '',
        'content': content or '',
    }, code=200, follow_redirects=True)

    if not title:
        aye('in', 'slug is required', c.data)
        aye('in', 'title is required', c.data)
    else:
        node = Node.fetch_one({'slug': slugify(title)})
        aye(True, node)
        return node


def test_node_new():
    clear_db([Node, app.db.Text, app.db.TextBit])

    add_node('')

    text = test_text.add_text()[0]
    node = add_node(content=text['_id'])
    aye(True, node['_id'])
    aye('==', node['content'], text)
    aye('==', app.user, node['owner'])
    aye('==', c.path, app.url_for(':node.edit', id=node['_id']))

    add_node()
    aye('in', 'duplicate key error index', c.data)

    node1 = add_node('test title #1', parent=node.full_slug())
    aye('==', node, node1['parent'])
    aye('==', app.user, node1['owner'])
    aye('in', 'value="%s"' % node.full_slug(), c.data)

    node2 = add_node(u'тест тайтл #2', parent=node.full_slug())
    aye('==', node, node2['parent'])
    aye('==', app.user, node2['owner'])
    aye('in', 'value="%s"' % node.full_slug(), c.data)

    node21 = add_node('test title #21', parent=node2.full_slug())
    aye('==', node2, node21['parent'])
    aye('==', app.user, node21['owner'])
    aye('in', 'value="%s"' % node2.full_slug(), c.data)

    return node, node1, node2, node21


def test_node_with_text():
    clear_db([Node, app.db.Text, app.db.TextBit])

    text = test_text.add_text()[0]
    text_id = text['_id']
    c.get(app.url_for(':node.edit'), query_string={
        'content': text_id
    }, code=200)
    aye('in', 'value="%s"' % text_id, c.data, c.url)
    node = add_node(content=text_id)

    c.get(app.url_for(':text.show', id=text_id), code=200)
    aye('in', node['title'], c.data)

    c.get(app.url_for(':text.delete', id=text_id), code=302)
    node.reload()
    aye('is', None, node['content'])

    c.get(app.url_for(':text.edit'), query_string={
        'node': str(node['_id'])
    }, code=200)
    node.reload()
    aye(True, node['content'])


def test_node_new_fails():
    clear_db([Node])

    c.post(app.url_for(':node.edit'), data={'title': ''}, code=400)

    node = add_node()
    node.delete()
    c.get(app.url_for(':node.edit', id=node['_id']), code=404)


def test_node_show():
    node, node1, node2, node21 = test_node_new()
    slug = node['slug']
    slug1 = '/'.join([slug, node1['slug']])
    slug2 = '/'.join([slug, node2['slug']])
    slug21 = '/'.join([slug2, node21['slug']])

    c.get(app.url_for(':node.show', slug=slug), code=200)
    aye('in', '<h1>%s' % node['title'], c.data)
    aye('in', slug1, c.data)
    aye('in', slug2, c.data)
    aye('in', node['content'].html, c.data)

    c.get(app.url_for(':node.show', slug=slug1), code=200)
    aye('in', '<h1>%s' % node1['title'], c.data)

    c.get(app.url_for(':node.show', slug=slug2), code=200)
    aye('in', '<h1>%s' % node2['title'], c.data)
    aye('in', slug21, c.data)

    c.get(app.url_for(':node.show', slug=slug21), code=200)
    aye('in', '<h1>%s' % node21['title'], c.data)


def test_node_show_fails2():
    test_node_new()
    c.get(app.url_for(':node.show', slug='test/test1/test2'), code=404)
    c.get(app.url_for(':node.show', slug='test1'), code=404)
    c.get(app.url_for(':node.show', slug='test/test21'), code=404)
