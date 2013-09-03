from docutils import core, nodes
from docutils.parsers.rst import directives, Directive
from markdown2 import Markdown
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers.special import TextLexer


def markdown(text):
    md = Markdown(extras=['footnotes', 'code-friendly', 'code-color'])
    return md.convert(text)


def rst(source, source_path=None):
    Pygments.register('code-block')

    parts = core.publish_parts(
        source=source,
        source_path=source_path,
        writer_name='html',
        settings_overrides={
            'footnote_references': 'superscript',
            'traceback': True
        }
    )
    return parts['title'], parts['body']


class Pygments(Directive):
    """Source code syntax hightlighting."""
    inline_styles = True
    formatters = {
        'default': HtmlFormatter(noclasses=inline_styles),
        'number': HtmlFormatter(noclasses=inline_styles, linenos=True),
    }

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'number': directives.flag}
    has_content = True

    def run(self):
        self.assert_has_content()
        try:
            lexer = get_lexer_by_name(self.arguments[0])
        except ValueError:
            # no lexer found - use the text one instead of an exception
            lexer = TextLexer()

        formatter = self.options.popitem()[0] if self.options else 'default'
        formatter = self.formatters[formatter]
        parsed = highlight(u'\n'.join(self.content), lexer, formatter)
        return [nodes.raw('', parsed, format='html')]

    @classmethod
    def register(cls, name):
        directives.register_directive(name, cls)
