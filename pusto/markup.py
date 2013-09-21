from docutils.core import publish_parts
from markdown2 import Markdown


def markdown(text):
    md = Markdown(extras=['footnotes', 'code-friendly', 'code-color'])
    return md.convert(text)


def rst(source, source_path=None):
    parts = publish_parts(
        source=source,
        source_path=source_path,
        writer_name='html',
        settings_overrides={
            'footnote_references': 'superscript',
            'syntax_highlight': 'short',
            'smart_quotes': 'yes',
            'cloak_email_addresses': True,
            'traceback': True
        }
    )
    return parts['title'], parts['body']
