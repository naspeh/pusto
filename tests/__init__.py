from naya.helpers import marker
from naya.script import sh
from naya.testing import aye

from pusto import App as _App


class App(_App):
    @marker.pre_request.index(0)
    def session_load(self):
        if not hasattr(self, 'session'):
            self.session = {}

    @marker.post_request()
    def session_save(self, response):
        pass


app = App(prefs={
    'testing': True,
    'mongo': {'db': 'test_pusto'}
})

client = app.test_client(url='/resume/')


def clear_db(docs=None):
    if not docs:
        docs = app.mongo._registered_documents.values()

    for doc in docs:
        doc.collection.drop()

    app.mongo_init()


def init_db():
    sh('mongorestore -d{0} {1}'.format(
        app['mongo:db'], app.get_path('..', 'dump', 'pusto')
    ))


def authorize(name=u'naspeh'):
    name = unicode(name)
    app.session_load()
    app.openid_complete({'email': u'%s@ya' % name, 'name': name})
    client.get('/')
    aye('==', name, app.user['name'])
