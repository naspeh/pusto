import re
from datetime import datetime

from mongokit import Document as _Document, IS
from naya.helpers import marker
from werkzeug import Href

from . import markup
from .ext.translit import slugify


class Document(_Document):
    collection = None
    app = None
    use_autorefs = True
    force_autorefs_current_db = True

    @property
    def dbref(self):
        return self.get_dbref()

    def is_valid(self, field=None):
        self.validation_errors = {}
        self.raise_validation_errors = False
        self.validate()
        self.raise_validation_errors = True
        if field:
            return field not in self.validation_errors
        else:
            return not bool(self.validation_errors)

    def by_id(self, id):
        id = self.app.object_id(id)
        if not id:
            return None
        return self.get_from_id(id) if id else None

    def pre_delete(self):
        pass

    def delete(self, *args, **kwargs):
        self.pre_delete()
        super(Document, self).delete(*args, **kwargs)


class CreatedMixin(Document):
    structure = {
        'created': datetime,
    }
    required_fields = ['created']
    default_values = {'created': datetime.utcnow}
    indexes = [
        {'fields': [('created', -1)]},
    ]


@marker.model()
class User(CreatedMixin):
    __collection__ = 'users'

    structure = {
        'email': unicode,
        'name': unicode
    }
    required_fields = ['email', 'name']
    indexes = [
        {'fields': ['email'], 'unique': True},
        {'fields': ['name'], 'unique': True}
    ]


class OwnerMixin(Document):
    structure = {
        'owner': User
    }


class MarkupMixin(Document):
    structure = {
        'markup': IS(u'rst', u'markdown'),
    }
    required_fields = ['markup']
    default_values = {'markup': u'rst'}


@marker.model()
class TextBit(CreatedMixin):
    __collection__ = 'text_bits'

    BIT_HIDE = '<div class="bit-hide"><pre>%s</pre></div>'

    structure = {
        'body': unicode,
        'type': IS(u'global', u'code', u'quote')
    }
    required_fields = ['body']

    @property
    def text(self):
        return self.app.db.Text.one({'bits': self.dbref})

    @property
    def html(self):
        text = self.text
        bodies = [self['body']]
        for bit in text['bits']:
            if bit['type'] == 'global' and bit != self:
                bodies.append(bit['body'])

        bodies = '\n\n'.join(bodies)

        html = getattr(markup, text['markup'])(bodies)
        if not html.strip():
            html = self.BIT_HIDE % self['body']
        return html

    def pre_delete(self):
        text = self.text
        for bit in text['bits']:
            if bit['_id'] == self['_id']:
                text['bits'].remove(bit)
        text.save()

    def save_all(self, text):
        bodies = re.split(r'\n{2}\.\. _bit[-\d+]*:\n{2}', self['body'])
        for body in bodies[:-1]:
            bit_new = self.app.db.TextBit(self.copy())
            if '_id' in bit_new:
                del bit_new['_id']
            bit_new['body'] = body
            bit_new.save()
            text['bits'].insert(text['bits'].index(self), bit_new)

        self['body'] = bodies[-1]
        self.save()


@marker.model()
class Text(MarkupMixin, CreatedMixin, OwnerMixin):
    __collection__ = 'texts'

    BIT_BEGIN = '.. _bit-%s:\n\n'

    structure = {
        'bits': [TextBit],
    }

    @property
    def node(self):
        return self.app.db.Node.one({'content': self.get_dbref()})

    @property
    def html(self):
        return markup.rst(self.src)

    @property
    def src(self):
        src = []
        for i in xrange(len(self['bits'])):
            body = self['bits'][i]['body']
            if i == 0:
                src.append(body)
            else:
                src.append(self.BIT_BEGIN % i + body)
        return '\n\n'.join(src)

    @property
    def url_edit(self):
        return self.app.url_for(':text.edit', id=self['_id'])

    def bit_by_id(self, bit_id):
        bit_id = self.app.object_id(bit_id)
        for bit in self['bits']:
            if '_id' in bit and bit['_id'] == bit_id:
                return bit
        return None

    def pre_delete(self):
        node = self.node
        if node:
            node['content'] = None
            node.save()
        for bit in self['bits']:
            bit.delete()


@marker.model()
class Node(CreatedMixin, OwnerMixin):
    __collection__ = 'nodes'

    structure = {
        'title': unicode,
        'slug': unicode,
        'urls': [unicode],
        'published': datetime,
        'content': Text
    }
    required_fields = ['title', 'slug']

    @property
    def children(self):
        return self.app.db.Node.fetch({'parent': self.get_dbref()})

    @property
    def full_slug(self):
        if '_id' not in self:
            raise KeyError('Node not saved')

        slug = [self['slug']]
        if self['parent']:
            slug.insert(0, self['parent'].full_slug)
        return '/'.join(slug)

    @property
    def url_edit(self):
        text_id = self['content'] and self['content']['_id'] or None
        url = self.app.url_for(':text.edit', id=text_id)
        if not text_id:
            url = Href(url)(node=self['_id'])
        return url

    @property
    def url_show(self):
        return self.app.url_for(':node.show', slug=self.full_slug)

    def prepare_slug(self):
        if not self['slug'] and self['title']:
            self['slug'] = slugify(self['title'])

    def save(self, *args, **kwargs):
        self.prepare_slug()
        super(Node, self).save(*args, **kwargs)

    def by_slug(self, flat_slug):
        slugs = flat_slug.strip('/').split('/')
        parent = None
        for slug in slugs:
            parent = None if parent is None else parent
            parent_doc = self.one({'slug': slug, 'parent': parent})
            if not parent_doc:
                return None
            parent = parent_doc.get_dbref()
        return parent_doc

Node.structure['parent'] = Node
Node.indexes = [{
    'fields':['parent', 'slug'],
    'unique':True,
}]
