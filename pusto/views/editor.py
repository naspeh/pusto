from naya import UrlMap


map = UrlMap(__name__)


@map.route('/')
def main(app):
    text = app.db.Text.fetch_one()
    return app.to_template('editor/main.html', text=text)


@map.route('/bit/add/', defaults={'id': None})
@map.route('/bit/<id>')
def bit(app, id):
    if id is None:
        text = app.db.Text.fetch_one()
        bit = app.db.TextBit()
        bit['body'] = app.request.form['body']
        bit.save()
        text['bits'].append(bit)
        text.save()
    return app.from_template('editor/partial.html', 'viewer')(text, bit)
