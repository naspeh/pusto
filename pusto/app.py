from naya.helpers import marker


class AppMixin(object):
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
