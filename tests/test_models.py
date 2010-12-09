from datetime import datetime

from naya.testing import raises
from pymongo.errors import DuplicateKeyError

from . import app
from pusto.translit import slugify


def setup():
    app.mongo.drop_database(app['mongo:db'])


def is_created(doc):
    assert isinstance(doc['created'], datetime)


def is_markuped(doc):
    assert doc.is_valid('markup')
    assert doc['markup'] == u'rst'
    doc['markup'] = 'textile'
    assert not doc.is_valid('markup')
    doc['markup'] = u'markdown'
    assert doc.is_valid('markup'), doc.validation_errors


def test_node(title=u'test title'):
    node = app.db.Node()
    is_created(node)
    assert not node.is_valid()
    node.update({'title': title, 'content': test_text()})
    node.save()
    assert node['slug'] == slugify(title)
    assert '_id' in node

    node['wrong'] = True
    assert not node.is_valid()

    node2 = app.db.Node()
    node2['title'] = title
    raises(DuplicateKeyError, lambda: node2.save())
    return node


def test_text():
    bit = app.db.TextBit()
    is_created(bit)
    is_markuped(bit)
    assert not bit.is_valid()
    bit['body'] = u'test body'
    bit.save()
    assert '_id' in bit

    text = app.db.Text()
    is_created(text)
    is_markuped(text)
    assert text.is_valid()
    text.update({'bits': [bit]})
    text.save()
    assert '_id' in text
