from lxml import html
from naya.helpers import marker


class AppMixin(object):
    def partial(self, selector, html_):
        def to_unicode(element):
            return html.tostring(element, encoding='utf-8').decode('utf-8')

        result = html.fromstring(html_).cssselect(selector)
        result = [to_unicode(el) for el in result]
        return '\n'.join(result)

    def maybe_partial(self, selector, html_,):
        if not self.request.is_xhr:
            return html_
        return self.partial(selector, html_)

    def part_template(self, template_name, selector, **context):
        html_ = self.to_template(template_name, **context)
        return self.partial(selector, html_)

    @marker.middleware()
    def profile_middleware(self, dispatch):
        if not self['profiler']:
            return dispatch

        from repoze.profile.profiler import AccumulatingProfileMiddleware

        return AccumulatingProfileMiddleware(
            dispatch,
            log_filename=self.get_path('..', 'var', 'profile.log'),
            cachegrind_filename=self.get_path('..', 'var', 'cachegrind.out'),
            discard_first_request=False,
            flush_at_shutdown=True,
            path='/__profile__'
        )
