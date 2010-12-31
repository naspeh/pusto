from docutils import nodes
from docutils.parsers.rst import directives, Directive
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers.special import TextLexer


class Pygments(Directive):
    """Source code syntax hightlighting."""
    inline_styles = False
    formatters = {
        'default': HtmlFormatter(noclasses=inline_styles),
        'linenos': HtmlFormatter(noclasses=inline_styles, linenos=True),
    }

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = dict((key, directives.flag) for key in formatters.keys()[1:])
    has_content = True

    def run(self):
        self.assert_has_content()
        try:
            lexer = get_lexer_by_name(self.arguments[0])
        except ValueError:
            # no lexer found - use the text one instead of an exception
            lexer = TextLexer()

        formatter = self.options and self.options.keys()[0] or 'default'
        formatter = self.formatters[formatter]
        parsed = highlight(u'\n'.join(self.content), lexer, formatter)
        return [nodes.raw('', parsed, format='html')]

    @classmethod
    def register(cls, name):
        directives.register_directive(name, cls)
