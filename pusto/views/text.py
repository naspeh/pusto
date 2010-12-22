from naya.helpers import marker


@marker.route('/new', defaults={'id': 'new'})
@marker.route('/<id>/edit')
def edit(app, id):
    node = None
    if 'node' in app.request.args:
        node = app.request.args['node']
    text, node = prepare(id, app, node)
    bit = prepare_bit('new', text, app)
    return app.to_template('text/edit.html', text=text, active=bit, node=node)


@marker.route('/<id>/delete')
def delete(app, id):
    text = prepare(id, app)[0]
    text.delete()
    return app.redirect(app.url_for(':text.edit'))


@marker.route('/<id>')
def show(app, id):
    text, node = prepare(id, app)
    return app.maybe_partial(
        app.to_template('text/show.html', text=text, node=node), '#text-show'
    )


@marker.route('/<id>/bit')
def bit(app, id):
    data = app.request.form
    if not data:
        app.abort(403)

    action = data['action']
    bit_id = data['bit']
    text, node = prepare(id, app)
    bit = prepare_bit(bit_id, text, app)
    if action == 'apply':
        if bit['_id'] is None:
            del bit['_id']
        insert = data['insert']
        if insert:
            text['bits'].remove(bit)
            parent = data['parent']
            parent = app.db.TextBit.by_id(parent)
            parent = text['bits'].index(parent)
            parent = parent if insert == 'before' else parent + 1
            text['bits'].insert(parent, bit)

        bit['body'] = data['body']
        bit.save()
        text.save()

        prepare_bit('new', text, app)
    elif action == 'delete' and bit_id != 'new':
        bit.delete()
        bit = prepare_bit('new', text, app)
    elif action == 'reset':
        return bit['body']
    return app.maybe_partial(
        app.to_template('text/edit.html', text=text, node=node, active=bit),
        '#text-edit'
    )


def prepare(id, app, node_id=None):
    node = None
    if id == 'new':
        text = app.db.Text()
        text.update({'owner': app.user})
    else:
        text = app.db.Text.by_id(id) if id else None
        node = text and text.node or None
    if not node and node_id:
        node = app.db.Node.by_id(node_id)
        if not node:
            return app.abort(404)
        text.save()
        node['content'] = text
        node.save()
    if not text:
        return app.abort(404)
    return text, node or app.db.Node()


def prepare_bit(id, text, app):
    if id == 'new':
        bit = app.db.TextBit()
        bit['body'] = ''
        bit['_id'] = None
        text['bits'].append(bit)
    else:
        bit = app.db.TextBit.by_id(id) if id else None
    if not bit:
        return app.abort(404)
    return bit
