#!/usr/bin/python3

from pymongo import MongoClient
import os
import pprint
import yaml

from .. import config


def main(args):
    blueprint_file = os.path.join(config.SDE_PATH, 'fsd/blueprints.yaml')

    with open(blueprint_file) as data:
        all_data = yaml.load(data)

    mongo_client = MongoClient('mongodb://%s:27017' % config.MONGO_IP)
    db = mongo_client[config.MONGODB]
    bptable = db[config.MONGOBLUEPRINTS]

    for bpid, therest in all_data.items():
        record = {}
        record['itemid'] = bpid
        #the which research tech 3 have an odd setup compared to other bp's
        #this let me skip them...
        try:
            for key, value in therest['activities']['manufacturing'].items():
                #component is a list of dictionaries
                #where each dict is
                #typeid mapped to a int for the type of item need
                #quantity maped to an int of how many of that item is needed
                record[key] = value
        except Exception as e:
            pprint.pprint(therest)
            continue
        try:
            bptable.insert_one(record)
        except Exception as e:
            print('failed to insert record')
            pprint.pprint(record)
    mongo_client.close()


if __name__ == '__main__':
    main(None)