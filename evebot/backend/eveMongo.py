#!/usr/bin/python3

from pymongo import MongoClient

from evebot import config

class EveMongo(object):
    #we can do more with this, this is a shell for basic functionality
    def __init__(self, collection_name):
        mongo_client = MongoClient('mongodb://%s:27017' % config.MONGO_IP)
        self.database = mongo_client[config.MONGODB]
        self.collection = collection_name


    @property
    def collection(self):
        return self._collection


    @collection.setter
    def collection(self, collection_name):
        self._collection_name = collection_name
        self._collection = self.database[self._collection_name]

