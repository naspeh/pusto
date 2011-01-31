from naya.helpers import marker


REDIRECTS = (
    ('/post/avtozagruzka-klassov-v-prilozheniyah-na-zend-framework/',
    'blog/2008/09/25/avtozagruzka-klassov-v-prilozheniyah-na-zend-framework',
    'r/zf-autoload'),
    ('/post/unikalniy-nick/', 'r/nick'),
)


@marker.defaults()
def defaults():
    return {
        'theme': {'path_suffix': '_data'},
        'jinja': {'path_suffix': '_data'}
    }


class StaticMixin(object):
    @marker.pre_request()
    def redirector(self):
        path = self.request.path.strip('/')
        for paths in REDIRECTS:
            if path in paths:
                return self.redirect(paths[0], code=301)
