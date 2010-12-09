from datetime import datetime

from mongokit import Document as BaseDocument, IS
from naya.helpers import marker

from . import markup
from .ext.translit import slugify


class Document(BaseDocument):
    def is_valid(self, field=None):
        self.validation_errors = {}
        self.raise_validation_errors = False
        self.validate()
        self.raise_validation_errors = True
        if field:
            return field not in self.validation_errors
        else:
            return not bool(self.validation_errors)


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
        'username': unicode
    }
    required_fields = ['email', 'username']
    indexes = [
        {'fields': ['email'], 'unique': True},
        {'fields': ['username'], 'unique': True}
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
class TextBit(MarkupMixin, CreatedMixin):
    __collection__ = 'text_bits'

    structure = {
        'body': unicode
    }
    required_fields = ['body']

    @property
    def html(self):
        return getattr(markup, self['markup'])(self['body'])


@marker.model()
class Text(MarkupMixin, CreatedMixin, OwnerMixin):
    __collection__ = 'texts'

    structure = {
        'bits': [TextBit],
    }
    use_autorefs = True
    force_autorefs_current_db = True


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
    use_autorefs = True
    force_autorefs_current_db = True

    def prepare_slug(self):
        if not self['slug'] and self['title']:
            self['slug'] = slugify(self['title'])

    def save(self, *args, **kwargs):
        self.prepare_slug()
        super(Node, self).save(*args, **kwargs)

Node.structure['parent'] = Node
Node.indexes = [{
    'fields':['parent', 'slug'],
    'unique':True,
}]
