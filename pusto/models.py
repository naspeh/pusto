from datetime import datetime

from mongokit import Document


class Timed(Document):
    structure = {
        'created_at': datetime,
        'updated_at': datetime
    }
    required_fields = ['created_at']
    default_values = {'created_at': datetime.utcnow}


class TextBit(Timed):
    __collection__ = 'texts'

    structure = {
        'body': unicode
    }
    required_fields = ['body']
    dot_notation_warning = True


class Text(Timed):
    __collection__ = 'texts'

    structure = {
        'bits': [TextBit]
    }
    required_fields = ['bits']
    dot_notation_warning = True
