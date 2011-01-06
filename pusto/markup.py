from docutils import core
from lxml import html
from markdown2 import Markdown

from ext.rst import Pygments


def markdown(text):
    md = Markdown(extras=['footnotes', 'code-friendly', 'code-color'])
    return md.convert(text)


def rst(text, as_document=True):
    Pygments.register('sourcecode')

    parts = core.publish_parts(source=text, writer_name='html',
        settings_overrides={
            'footnote_references': 'superscript',
            'traceback': True
        }
    )
    result = html.fromstring(parts['html_body'])
    result = '\n'.join(html.tostring(i) for i in result.iterchildren())
    if as_document:
        result = '<div class="document">%s</div>' % result
    return result
