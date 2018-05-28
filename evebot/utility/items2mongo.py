#!/usr/bin/python3

from .. import config
from ..connectors import evemongo

from pymongo import MongoClient
import os
import yaml


def main(args):
    typeid_file = os.path.join(config.SDE_PATH, 'fsd/typeIDs.yaml')

    with open(typeid_file) as content:
        all_data = yaml.load(content)

    all_records = []
    for typeid, data in all_data.items():
        record = {}
        record['typeid'] = typeid
        if data['published']:
            #fails to import any tech 3 subsystem
            for key, val in data.items():
                if key in ['description', 'name']:
                    record[key] = val['en']
                else:
                    record[key] = val
            all_records.append(record)


    mongo_client = MongoClient('mongodb://%s:27017' % config.MONGO_IP)
    db = mongo_client[config.MONGODB]
    itemtable = db[config.MONGOITEMS]
    for record in all_records:
        try:
            itemtable.insert_one(record)
        except Exception as e:
            print('failed to insert %s' % record)
    mongo_client.close()


if __name__ == '__main__':
    main(None)