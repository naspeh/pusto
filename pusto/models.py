from datetime import datetime

from mongokit import Document as BaseDocument, IS

from . import markup
from .translit import slugify


class Document(BaseDocument):
    raise_validation_errors = False

    def is_valid(self, field=None):
        self.validation_errors = {}
        self.validate()
        if field:
            return field not in self.validation_errors
        else:
            return not bool(self.validation_errors)


class Created(Document):
    structure = {
        'created': datetime,
    }
    required_fields = ['created']
    default_values = {'created': datetime.utcnow}


class Node(Created):
    __collection__ = 'nodes'

    structure = {
        'title': unicode,
        'slug': unicode,
        'urls': [unicode],
        'published': datetime
    }
    required_fields = ['title', 'slug']
    use_autorefs = True

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


class Markup(Document):
    structure = {
        'markup': IS(u'rst', u'markdown'),
    }
    required_fields = ['markup']
    default_values = {'markup': u'rst'}


class TextBit(Markup, Created):
    __collection__ = 'text_bits'

    structure = {
        'body': unicode
    }
    required_fields = ['body']

    @property
    def html(self):
        return getattr(markup, self['markup'])(self['body'])


class Text(Markup, Created):
    __collection__ = 'texts'

    structure = {
        'node': Node,
        'bits': [TextBit],
    }
    use_autorefs = True
