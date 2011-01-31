from datetime import datetime

from naya.helpers import marker
from pymongo.errors import DuplicateKeyError


@marker.authorized(as_admin=True)
@marker.route('/node/new/', defaults={'id': 'new'})
@marker.route('/node/<id>/edit/')
def edit(app, id):
    node = prepare(app, id)
    errors = []
    data = app.request.form
    if data:
        published = data.get('published', None) and datetime.utcnow() or None

        slugs = data['slug'].strip().split('/')
        slug = slugs and slugs[-1] or None
        parent = slugs and slugs[:-1] or None
        if parent:
            parent = app.db.Node.by_slug('/'.join(parent))

        node.update({
            'owner': app.user,
            'parent': parent,
            'title': data['title'].strip() or None,
            'slug': slug,
            'content': app.db.Text.by_id(data['content'].strip()),
            'published': published
        })
        node_ = node.copy()
        node.prepare_slug()
        if node.is_valid():
            try:
                node.save()
                if not app.request.is_xhr:
                    return app.redirect(':node.edit', id=node['_id'])
            except DuplicateKeyError, e:
                errors = [e]
                node = node_
        else:
            for error in node.validation_errors.values():
                errors += error

        content = node['content']
    elif '_id' in node:
        content = node['content']
    elif 'content' in app.request.args:
        content = app.db.Text.by_id(app.request.args['content'])
    else:
        content = None

    return app.to_template('node/edit.html',
        node=node, content=content, errors=errors,
    )


@marker.route('/a/<path:slug>/')
def show(app, slug):
    node = app.db.Node.by_slug(slug)
    if not node:
        return app.abort(404)
    return app.to_template('node/show.html', node=node)


@marker.authorized(as_admin=True)
@marker.route('/nodes/')
def roll(app):
    nodes = app.db.Node.find({'parent': None})
    return app.to_template('node/list.html', nodes=nodes)


def prepare(app, id):
    if id == 'new':
        node = app.db.Node()
    else:
        node = app.db.Node.by_id(id.strip()) if id else None
    if not node:
        return app.abort(404)
    return node
