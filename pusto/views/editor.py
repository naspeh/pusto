from mongokit import ObjectId

from naya import UrlMap


map = UrlMap(__name__)


@map.route('/')
def main(app):
    text, bit = prepare('new', app)
    return app.to_template('editor/main.html', text=text, active=bit)


@map.route('/bit')
def bit(app):
    if not app.request.form:
        app.abort(403)

    action = app.request.form['action']
    id = app.request.form['bit']
    text, bit = prepare(id, app)
    if action == 'apply':
        if bit['_id'] is None:
            del bit['_id']
        insert = app.request.form['insert']
        if insert:
            text['bits'].remove(bit)
            parent = app.request.form['parent']
            parent = app.db.TextBit.find_one(ObjectId(parent))
            parent = text['bits'].index(parent)
            parent = parent if insert == 'before' else parent + 1
            text['bits'].insert(parent, bit)

        bit['body'] = app.request.form['body']
        bit.save()
        text.save()
        prepare_bit(text, app)
    elif action == 'delete' and id != 'new':
        bit.delete()
        text['bits'].remove(bit)
        text.save()
        bit = prepare_bit(text, app)
    elif action == 'reset':
        return bit['body']
    return app.from_template('editor/partial.html', 'partial')(text, bit, app)


def prepare(id, app):
    text = app.db.Text.fetch_one()
    text = text and text or app.db.Text()
    if id == 'new':
        bit = prepare_bit(text, app)
    else:
        bit = app.db.TextBit.find_one(ObjectId(id))
    return text, bit


def prepare_bit(text, app):
    bit = app.db.TextBit()
    bit['body'] = ''
    bit['_id'] = None
    text['bits'].append(bit)
    return bit
