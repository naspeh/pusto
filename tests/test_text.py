from naya.testing import aye, call
from nose import with_setup

from . import app


c = app.test_client()


def setup_db():
    test_db = 'test_pusto'
    app.mongo.drop_database(test_db)
    app.db = app.mongo[test_db]


def add_text():
    c.get(app.url_for(':text.edit'), code=200)
    aye('==', app.db.Text.fetch().count(), 0)
    aye('==', app.db.TextBit.fetch().count(), 0)

    return add_bit('new', 'new')


def add_bit(text_id, bit_id, body='body', number=1, insert='', parent=''):
    c.post(app.url_for(':text.bit', id=text_id), data={
        'bit': bit_id,
        'action': 'apply',
        'body': body,
        'insert': insert,
        'parent': parent
    }, code=200)
    aye('==', app.db.Text.fetch().count(), 1)
    text = app.db.Text.fetch_one()
    aye('==', number, call(len, text['bits']))
    aye('==', app.db.TextBit.fetch().count(), number)
    if bit_id == 'new':
        bit = list(app.db.TextBit.fetch())[-1]
    else:
        bit = app.db.TextBit.find_one(app.object_id(bit_id))
    aye('==', bit['body'], body)
    return text, bit


@with_setup(setup_db)
def test_bit_new():
    text, bit = add_text()
    text, bit2 = add_bit(text['_id'], 'new', 'body2', 2)
    aye('==', bit['body'], text['bits'][0]['body'])
    aye('==', bit2['body'], text['bits'][1]['body'])


@with_setup(setup_db)
def test_bit_edit():
    text, bit = add_text()
    text, bit2 = add_bit(text['_id'], bit['_id'], 'body.v2')
    aye('==', bit['_id'], bit2['_id'])
    aye('==', bit2['body'], text['bits'][0]['body'])


@with_setup(setup_db)
def test_bit_before():
    text, bit = add_text()
    text, bit2 = add_bit(text['_id'], 'new', 'body2', 2, 'before', bit['_id'])
    aye('==', bit['body'], text['bits'][1]['body'])
    aye('==', bit2['body'], text['bits'][0]['body'])


@with_setup(setup_db)
def test_bit_after():
    text, bit = add_text()
    text, bit2 = add_bit(text['_id'], 'new', 'body2', 2)

    text, bit = add_bit(
        text['_id'], bit['_id'], bit['body'], 2, 'after', bit2['_id']
    )
    aye('==', bit['body'], text['bits'][1]['body'])
    aye('==', bit2['body'], text['bits'][0]['body'])


@with_setup(setup_db)
def test_bit_delete():
    text, bit = add_text()
    c.post(app.url_for(':text.bit', id=text['_id']), data={
        'bit': bit['_id'],
        'action': 'delete',
        'body': 'body2',
    }, code=200)
    aye('==', app.db.Text.fetch().count(), 1)
    aye('==', app.db.TextBit.fetch().count(), 0)

    text.reload()
    aye('==', 0, call(len, text['bits']))


@with_setup(setup_db)
def test_bit_reset():
    text, bit = add_text()
    body = 'body2'
    c.post(app.url_for(':text.bit', id=text['_id']), data={
        'bit': bit['_id'],
        'action': 'reset',
        'body': 'body2',
    }, code=200)
    aye('==', app.db.Text.fetch().count(), 1)
    aye('==', app.db.TextBit.fetch().count(), 1)

    text.reload()
    aye('==', 1, call(len, text['bits']))
    aye('!=', body, text['bits'][0]['body'])


@with_setup(setup_db)
def test_text_delete():
    text = add_text()[0]
    c.get(app.url_for(':text.delete', id=text['_id']))
    aye('==', app.db.Text.fetch().count(), 0)


DATA = {
    'bit': 'new',
    'action': 'apply',
    'body': 'body2',
    'insert': ''
}


def test_missing_data():
    for item in DATA.keys():
        data = DATA.copy()
        del data[item]
        c.post(app.url_for(':text.bit', id='new'), data=data, code=400)


def test_fails():
    c.post(app.url_for(':text.bit', id='test'), data=DATA, code=404)

    data = DATA.copy()
    data['bit'] = 'test'
    c.post(app.url_for(':text.bit', id='new'), data=data, code=404)

    c.get(app.url_for(':text.bit', id='new'), code=403)


@with_setup(setup_db)
def test_fails2():
    text = add_text()[0]
    c.get(app.url_for(':text.delete', id=text['_id']))
    c.post(app.url_for(':text.bit', id=text['_id']), data=DATA, code=404)
