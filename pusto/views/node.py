from datetime import datetime

from naya.helpers import marker
from pymongo.errors import DuplicateKeyError


@marker.authorized(as_admin=True)
@marker.route('/node/new', defaults={'id': 'new'})
@marker.route('/node/<id>/edit')
def edit(app, id):
    node = prepare(id, app)
    errors = []
    data = app.request.form
    if data:
        published = 'published' in data and data['published'] or None
        published = published and datetime.utcnow() or None

        node.update({
            'parent': app.db.Node.by_id(data['parent'].strip()),
            'title': data['title'].strip() or None,
            'slug': data['slug'].strip() or None,
            'content': app.db.Text.by_id(data['content'].strip()),
            'published': published
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


def prepare(id, app):
    if id == 'new':
        node = app.db.Node()
    else:
        node = app.db.Node.by_id(id.strip()) if id else None
    if not node:
        return app.abort(404)
    return node
