from lxml import html


class AppMixin(object):
    def maybe_partial(self, html_, selector):
        if not self.request.is_xhr:
            return html_
        return self.partial(html_, selector)

    def partial(self, html_, selector):
        result = html.fromstring(html_).cssselect(selector)
        result = [html.tostring(i) for i in result]
        return '\n'.join(result)

    def part_template(self, template_name, selector, **context):
        html_ = self.to_template(template_name, **context)
        return self.partial(html_, selector)
