from naya import Module


mod = Module(__name__)


@mod.route(
    '/blog/2008/09/25/avtozagruzka-klassov-v-prilozheniyah-na-zend-framework/',
    redirect_to='post/avtozagruzka-klassov-v-prilozheniyah-na-zend-framework/'
)
def redirect(app):
    pass
