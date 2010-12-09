from naya.helpers import marker
from pymongo.errors import DuplicateKeyError


@marker.route('/node/new', defaults={'id': 'new'})
@marker.route('/node/<id>/edit')
def edit(app, id):
    node = prepare(id, app)
    errors = []
    data = app.request.form
    if data:
        node.update({
            'parent': prepare_doc(app, app.db.Node, data['parent']),
            'title': data['title'].strip() or None,
            'slug': data['slug'].strip() or None,
            'content': prepare_doc(app, app.db.Text, data['content'])
        })
        node.prepare_slug()

        if node.is_valid():
            try:
                node.save()
                return app.redirect(':node.edit', id=str(node['_id']))
            except DuplicateKeyError, e:
                errors = [e]
        else:
            for error in node.validation_errors.values():
                errors += error
    return app.to_template('node/edit.html', node=node, errors=errors)


def prepare_doc(app, doc_type, flat_id):
    id = app.object_id(flat_id.strip())
    return doc_type.find_one(id) if id else None


def prepare(id, app):
    if id == 'new':
        node = app.db.Node()
    else:
        node = prepare_doc(app, app.db.Node, id)
    if not node:
        return app.abort(404)
    return node
