#!/usr/bin/python3

from pymongo import MongoClient

from .. import config

class EveMongo(object):

    def __init__(self, collection_name):
        self.mongo_client = MongoClient('mongodb://%s:27017' % config.MONGO_IP)
        self.database = self.mongo_client[config.MONGODB]
        self.collection = collection_name


    @property
    def collection(self):
        return self._collection


    @collection.setter
    def collection(self, collection_name):
        self._collection_name = collection_name
        self._collection = self.database[self._collection_name]


    def close(self):
        self.mongo_client.close()