import re
from datetime import datetime

from docutils.utils import SystemMessage
from jinja2.filters import do_striptags
from mongokit import Document as _Document, IS
from naya.helpers import marker
from pygments import highlight
from pygments.lexers import RstLexer
from pygments.formatters import HtmlFormatter
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
    _parent = None

    TYPES = u'global', u'hidden'
    BIT_ERROR = '<div class="system-message"><pre>%s</pre></div>'
    BIT_HIDE = '<div class="bit-hide">%s</div>'

    structure = {
        'body': unicode,
        'type': IS(*TYPES)
    }
    required_fields = ['body']

    @property
    def parent(self):
        if self._parent:
            return self._parent
        return self.app.db.Text.one({'bits': self.dbref})

    @property
    def pure_html(self):
        text = self.parent
        bodies = [self['body']]
        for bit in text['bits']:
            if bit['type'] == 'global' and bit != self:
                bodies.append(bit['body'])
        bodies = '\n\n'.join(bodies)

        try:
            html_ = markup.rst(bodies, as_bit=True)
        except SystemMessage as e:
            html_ = self.BIT_ERROR % e
        return html_

    @property
    def html(self):
        html_ = self.pure_html

        text = do_striptags(html_.strip())
        if not text.strip():
            html_ = highlight(self['body'], RstLexer(), HtmlFormatter())
            html_ = self.BIT_HIDE % html_

        if self['type'] == 'hidden':
            html_ = self.BIT_HIDE % html_
        return html_

    def pre_delete(self):
        text = self.parent
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
            bits = text['bits']
            if '_id' in self:
                bit = text.bit_by_id(self['_id'])
            else:
                bit = self
            bits.insert(bits.index(bit), bit_new)

        self['body'] = bodies[-1]
        self.save()


@marker.model()
class Text(MarkupMixin, CreatedMixin, OwnerMixin):
    __collection__ = 'texts'

    BIT_BEGIN = '.. _bit-%s:\n\n'

    structure = {
        'bits': [TextBit],
    }
    indexes = [{'fields': 'bits'}]

    @property
    def bits(self):
        for bit in self['bits']:
            bit._parent = self
        return self['bits']

    @property
    def node(self):
        return self.app.db.Node.one({'content': self.get_dbref()})

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
    def html(self):
        return '\n\n'.join(
            bit.pure_html.strip() for bit in self['bits']
                if bit['type'] not in TextBit.TYPES
        )

    @property
    def url_edit(self):
        return self.app.url_for(':text.edit', id=self['_id'])

    @property
    def url_copy(self):
        return self.app.url_for(':text.copy', id=self['_id'])

    @property
    def url_delete(self):
        return self.app.url_for(':text.delete', id=self['_id'])

    @property
    def url_show(self, src=None):
        return self.app.url_for(':text.show', id=self['_id'], src=src)

    def url_src(self, src=None):
        return self.app.url_for(':text.show', id=self['_id'], src=src)

    def bit_by_id(self, bit_id):
        bit_id = self.app.object_id(bit_id)
        for bit in self['bits']:
            if '_id' in bit and bit['_id'] == bit_id:
                return bit
        return None

    def bits_exlude(self, bit):
        bits = list(self['bits'])
        if bits.count(bit):
            bits.remove(bit)
        return bits

    def pre_delete(self):
        node = self.node
        if node:
            node['content'] = None
            node.save()
        for bit in self['bits']:
            bit.delete()

    def is_allow(self, user=None):
        user = user and user or self.app.user
        if self['owner'] == user or self.app.is_admin(user):
            return True
        return False


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
        return list(self.app.db.Node.fetch({'parent': self.get_dbref()}))

    @property
    def parent_children(self):
        children = self['parent'].children
        children.remove(self)
        return children

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
