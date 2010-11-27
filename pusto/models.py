from datetime import datetime

from mongokit import Document, IS

from . import markup


class Timed(Document):
    structure = {
        'created_at': datetime,
    }
    required_fields = ['created_at']
    default_values = {'created_at': datetime.utcnow}


class TextBit(Timed):
    __collection__ = 'text_bits'

    structure = {
        'markup': IS(u'rst', u'markdown'),
        'body': unicode
    }
    required_fields = ['markup', 'body']
    default_values = {'markup': u'rst'}

    @property
    def html(self):
        return getattr(markup, self['markup'])(self['body'])


class Text(Timed):
    __collection__ = 'texts'

    structure = {
        'bits': [TextBit]
    }
    use_autorefs = True
