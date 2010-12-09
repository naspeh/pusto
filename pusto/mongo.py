from mongokit import Connection, ObjectId
from pymongo.errors import InvalidId

from naya.helpers import marker


class MongoMixin(object):
    @marker.defaults()
    def mongo_defaults(self):
        return {'mongo': {
            'db': None,
            'models': []
        }}

    @marker.init()
    def mongo_init(self):
        self.mongo = Connection()
        self.db = self.mongo[self['mongo:db']]

        models = []
        for container in self['mongo:models']:
            models += [m[0] for m in marker.model.of(container)]
        self.mongo.register(models)

    def object_id(self, id):
        try:
            id = ObjectId(id)
        except InvalidId:
            id = None
        return id
