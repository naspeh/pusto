from lxml import html


class AppMixin(object):
    def partial(self, selector, html_):
        result = html.fromstring(html_).cssselect(selector)
        result = [html.tostring(i) for i in result]
        return '\n'.join(result)

    def maybe_partial(self, selector, html_,):
        if not self.request.is_xhr:
            return html_
        return self.partial(selector, html_)

    def part_template(self, template_name, selector, **context):
        html_ = self.to_template(template_name, **context)
        return self.partial(selector, html_)
