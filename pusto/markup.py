def markdown(text):
    from markdown2 import Markdown

    md = Markdown(extras=['footnotes', 'code-friendly', 'code-color'])
    return md.convert(text)


def rst(text):
    from docutils import core

    settings = {'footnote_references': 'superscript'}
    parts = core.publish_parts(
        source=text, writer_name='html', settings_overrides=settings
    )
    return parts['html_body']
