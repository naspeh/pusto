from datetime import datetime

from naya.testing import aye, raises
from pymongo.errors import DuplicateKeyError

from . import app, clear_db
from pusto.ext.translit import slugify


def setup():
    clear_db()


def is_created(doc):
    assert isinstance(doc['created'], datetime)


def is_markuped(doc):
    assert doc.is_valid('markup')
    assert doc['markup'] == u'rst'
    doc['markup'] = 'textile'
    assert not doc.is_valid('markup')
    doc['markup'] = u'markdown'
    assert doc.is_valid('markup'), doc.validation_errors


def test_user(name=u'naspeh'):
    user = app.db.User()
    is_created(user)
    assert not user.is_valid()
    user.update({'email': u'%s@ya' % name, 'name': name})
    user.save()
    assert user['_id']
    return user


def test_node(title=u'test title'):
    node = app.db.Node()
    is_created(node)
    assert not node.is_valid()

    name = u'naya'
    user = test_user(name)
    text = test_text(user)
    node.update({'title': title, 'content': text, 'owner': user})
    node.save()
    assert node['slug'] == slugify(title)
    assert node['_id']
    assert node['content']['_id']
    assert node['owner']['_id']

    node['wrong'] = True
    assert not node.is_valid()

    node2 = app.db.Node()
    node2['title'] = title
    raises(DuplicateKeyError, lambda: node2.save())

    raises(DuplicateKeyError, lambda: test_user(name))

    text.delete()
    aye('==', 0, app.db.Text.fetch().count())
    aye('==', 0, app.db.TextBit.fetch().count())
    node.reload()
    aye('is', None, node['content'])
    return node


def test_text(user=None):
    bit = app.db.TextBit()
    is_created(bit)
    assert not bit.is_valid()
    bit['body'] = u'test body'
    bit.save()
    assert bit['_id']

    text = app.db.Text()
    is_created(text)
    is_markuped(text)
    assert text.is_valid()
    text.update({'bits': [bit], 'owner': user or test_user(u'nayavu')})
    text.save()
    assert text['_id']
    assert text['owner']['_id']
    assert text['bits'][0]['_id']

    bit.delete()
    text.reload()
    aye('==', 0, app.db.TextBit.fetch().count())
    aye(False, text['bits'])
    return text


def add_bits(bits, text=app.db.Text):
    clear_db([app.db.User])

    text.update({'bits': bits, 'owner': test_user(u'nayavu')})
    text.save()
    return text


def test_global_bit():
    url = 'http://pusto.org'
    body = u'.. _pusto: %s' % url

    bit_glob = app.db.TextBit()
    bit_glob.update({'body': body, 'type': u'global'})
    bit_glob.save()

    bit = app.db.TextBit()
    bit['body'] = u'pusto_'
    bit.save()

    text = add_bits([bit_glob, bit])

    aye('in', body, bit_glob.html)
    aye('in', url, bit.html)
    aye('in', url, text.html)


def test_code_bit():
    bit = app.db.TextBit()
    bit['body'] = (
        u'.. sourcecode:: unknow\n'
        u'  :linenos:\n'
        u'\n'
        u'  from naya import Naya\n'
    )
    bit.save()

    add_bits([bit])
    aye('in', 'class="highlight', bit.html)
