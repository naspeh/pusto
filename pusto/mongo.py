from mongokit import Connection

from naya.helpers import register

from .models import TextBit, Text


class MongoMixin(object):
    @register('init')
    def mongo_init(self):
        self.mongo = Connection()
        self.db = self.mongo.pusto
        self.mongo.register([Text, TextBit])
