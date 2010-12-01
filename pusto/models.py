from datetime import datetime

from mongokit import Document, IS

from . import markup
from .translit import slugify


class Created(Document):
    structure = {
        'created': datetime,
    }
    required_fields = ['created']
    default_values = {'created': datetime.utcnow}


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
        'title': unicode,
        'slug': unicode,
        'urls': [unicode],
        'bits': [TextBit],
        'published': datetime
    }
    use_autorefs = True

    def prepare_slug(self):
        if not self['slug'] and self['title']:
            self['slug'] = slugify(self['title'])

    def save(self, *args, **kwargs):
        self.prepare_slug()
        super(Text, self).save(*args, **kwargs)
