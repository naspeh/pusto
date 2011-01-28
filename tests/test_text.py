import re

from naya.testing import aye, call
from nose import with_setup

from . import app, client as c, clear_db, authorize


def add_text(number=1):
    c.get(app.url_for(':text.edit'), code=200)
    aye('==', app.db.Text.fetch().count(), number - 1)
    aye('==', app.db.TextBit.fetch().count(), number - 1)

    return add_bit('new', 'new')


def add_bit(text_id, bit_id, body='body', number=1, data={}):
    url = app.url_for(':text.edit', id=text_id)
    c.get(url, code=200)
    aye('in', 'value="%s"' % url, c.data)

    data_ = {
        'bit': bit_id,
        'action': 'apply',
        'body': body,
    }
    data_.update(data)

    c.post(
        app.url_for(':text.bit', id=text_id),
        data=data_, code=200, follow_redirects=True
    )

    pattern = re.escape(app.url_for(':text.bit', id='new'))
    pattern = pattern.replace('new', '(\w*)')
    text_id = re.search(pattern, c.data)
    text_id = text_id.groups()[0]
    text = app.db.Text.by_id(text_id)
    aye('==', number, call(len, text['bits']))
    aye('==', app.user, text['owner'])
    aye('==', number, call(len, text['bits']))
    if bit_id == 'new':
        bit = list(app.db.TextBit.fetch())[-1]
    else:
        bit = app.db.TextBit.by_id(bit_id)
    aye('==', bit['body'], body)
    aye('in', text_id, app.session['texts'])
    aye('==', str(bit['_id']), app.session['texts'][text_id])
    return text, bit


@with_setup(clear_db)
def test_bit_new():
    authorize()
    text, bit = add_text()
    text, bit2 = add_bit(text['_id'], 'new', 'body2', 2, {'type': 'global'})
    aye('==', bit['body'], text['bits'][0]['body'])
    aye('==', bit2['body'], text['bits'][1]['body'])


@with_setup(clear_db)
def test_bit_edit():
    text, bit = add_text()
    text, bit2 = add_bit(text['_id'], bit['_id'], 'body.v2')
    aye('==', bit['_id'], bit2['_id'])
    aye('==', bit2['body'], text['bits'][0]['body'])


@with_setup(clear_db)
def test_bit_before():
    text, bit = add_text()
    text, bit2 = add_bit(text['_id'], 'new', 'body2', 2, {
        'insert': 'before', 'parent': bit['_id']
    })
    aye('==', bit['body'], text['bits'][1]['body'])
    aye('==', bit2['body'], text['bits'][0]['body'])


@with_setup(clear_db)
def test_bit_after():
    text, bit = add_text()
    text, bit2 = add_bit(text['_id'], 'new', 'body2', 2)

    text, bit = add_bit(text['_id'], bit['_id'], bit['body'], 2, {
        'insert': 'after', 'parent': bit2['_id']
    })
    aye('==', bit['body'], text['bits'][1]['body'])
    aye('==', bit2['body'], text['bits'][0]['body'])


@with_setup(clear_db)
def test_bit_delete():
    text, bit = add_text()
    c.post(app.url_for(':text.bit', id=text['_id']), data={
        'bit': bit['_id'],
        'action': 'delete',
        'body': 'body2',
    }, code=200)
    aye('==', app.db.Text.fetch().count(), 1)
    aye('==', app.db.TextBit.fetch().count(), 0)
    aye('not in', str(bit['_id']), c.data)

    text.reload()
    aye('==', 0, call(len, text['bits']))


@with_setup(clear_db)
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


@with_setup(clear_db)
def test_text_delete():
    text = add_text()[0]
    c.get(app.url_for(':text.delete', id=text['_id']))
    aye('==', app.db.Text.fetch().count(), 0)


@with_setup(clear_db)
def test_text_show():
    text = add_text()[0]
    text = add_bit(text['_id'], 'new', 'body2', 2)[0]

    url = app.url_for(':text.show', id=text['_id'])
    c.get(url, code=200)
    aye('in', '%s' % text['_id'], c.data)
    aye('in', text.html, c.data)
    aye('==', 1, call(c.data.count, 'class="document"'), c.data)
    aye(False, call(c.data.startswith, '<div id="text-show">'), c.data)

    c.get(url, code=200, headers=[('X_REQUESTED_WITH', 'XMLHttpRequest')])
    aye(True, call(c.data.startswith, '<div id="text-show-body">'), c.data)


@with_setup(clear_db)
def test_texts():
    authorize()
    texts = add_text()[0], add_text(number=2)[0]

    c.get(app.url_for(':text.roll'))
    for text in texts:
        aye('in', text.url_edit, c.data)


DATA = {'bit': 'new', 'action': 'apply', 'body': 'body2'}


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


@with_setup(clear_db)
def test_fails2():
    authorize()
    text = add_text()[0]

    authorize('forbidden')
    c.get(app.url_for(':text.delete', id=text['_id']), code=403)

    authorize()
    c.get(app.url_for(':text.delete', id=text['_id']))

    c.post(app.url_for(':text.bit', id=text['_id']), data=DATA, code=404)
    c.get(app.url_for(':text.edit', id=text['_id']), query_string={
        'node': 'wrong-node'
    }, code=404)
