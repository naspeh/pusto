from naya.helpers import marker

from pusto import App as _App


class App(_App):
    @marker.pre_request()
    def session_load(self):
        if not hasattr(self, 'session'):
            self.session = {}

    @marker.post_request()
    def session_save(self, response):
        pass


app = App(prefs={
    'mongo': {'db': 'test_pusto'}
})


def clear_db(docs=None):
    if not docs:
        docs = app.mongo._registered_documents.values()

    for doc in docs:
        doc.collection.drop()

    app.mongo_init()


def authorize(name=u'naspeh'):
    app.session_load()
    app.openid_complete({'email': u'%s@ya' % name, 'name': name})
