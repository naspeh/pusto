from mongokit import ObjectId

from naya import UrlMap


map = UrlMap(__name__)


@map.route('/')
def main(app):
    text = app.db.Text.fetch_one()
    text = text and text or app.db.Text()
    bit = get_bit('new', text, app)
    return app.to_template('editor/main.html', text=text, active=bit)


@map.route('/bit')
def bit(app):
    if not app.request.form:
        app.abort(403)

    id = app.request.form['bit']
    text = app.db.Text.fetch_one()
    text = text and text or app.db.Text()
    bit = get_bit(id, text, app)
    if app.request.form['action'] == 'apply':
        if '_id' in bit:
            del bit['_id']
        bit['body'] = app.request.form['body']
        bit.save()
        text.save()
    get_bit('new', text, app)
    return app.from_template('editor/partial.html', 'partial')(text, bit, app)


@map.route('/bit/<id>/src')
def bit_src(app, id):
    text = app.db.Text.fetch_one()
    bit = get_bit(id, text, app)
    if id != 'new':
        get_bit('new', text, app)
    return app.from_template('editor/partial.html', 'partial')(text, bit, app)


def get_bit(id, text, app):
    if id == 'new':
        bit = app.db.TextBit()
        bit['body'] = ''
        bit['_id'] = None
        text['bits'].append(bit)
    else:
        bit = app.db.TextBit.find_one(ObjectId(id))
    return bit
