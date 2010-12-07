from mongokit import Connection, ObjectId
from pymongo.errors import InvalidId

from naya.helpers import marker

from .models import Node, TextBit, Text


class MongoMixin(object):
    @marker.init()
    def mongo_init(self):
        self.mongo = Connection()
        self.db = self.mongo.pusto
        self.mongo.register([Node, Text, TextBit])

    def object_id(self, id):
        try:
            id = ObjectId(id)
        except InvalidId:
            id = None
        return id
