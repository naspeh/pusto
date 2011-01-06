import re

from docutils import core
from markdown2 import Markdown

from ext.rst import Pygments


def markdown(text):
    md = Markdown(extras=['footnotes', 'code-friendly', 'code-color'])
    return md.convert(text)


def rst(text, as_bit=False):
    Pygments.register('sourcecode')

    parts = core.publish_parts(source=text, writer_name='html',
        settings_overrides={
            'footnote_references': 'superscript',
            'traceback': True
        }
    )
    result = parts['html_body']
    if as_bit:
        result = re.sub(r'(^<div.+?class="document".*?>|<\/div>$)', '', result)
    return result
