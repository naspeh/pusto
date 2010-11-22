from datetime import datetime

from mongokit import Document


class Timed(Document):
    structure = {
        'created_at': datetime,
    }
    required_fields = ['created_at']
    default_values = {'created_at': datetime.utcnow}


class TextBit(Timed):
    __collection__ = 'text_bits'

    structure = {
        'body': unicode
    }
    required_fields = ['body']


class Text(Timed):
    __collection__ = 'texts'

    structure = {
        'bits': [TextBit]
    }
    use_autorefs = True
