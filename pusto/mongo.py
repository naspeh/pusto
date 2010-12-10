from mongokit import Connection

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
            for model in marker.model.of(container):
                model = model[0]
                models.append(model)
                model.collection = self.db[model.__collection__]

        self.mongo.register(models)
