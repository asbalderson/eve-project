#!/usr/bin/python3

from .. import config
from ..connectors import evemongo

import pprint
import os
import yaml


def main(args):
    typeid_file = os.path.join(config.SDE_PATH, 'fsd/typeIDs.yaml')

    with open(typeid_file) as content:
        all_data = yaml.load(content)

    eve_mongo = evemongo.EveMongo(config.MONGOITEMS)
    eve_mongo.collection.delete_many({})

    for typeid, data in all_data.items():
        record = {}
        record['typeid'] = typeid
        if data['published']:
            #fails to import any tech 3 subsystem
            for key, val in data.items():
                if key in ['description', 'name']:
                    record[key] = val['en'].lower()
                elif type(val) in (list, dict):
                    pass
                else:
                    record[key] = val
            try:
                eve_mongo.collection.insert_one(record)
            except Exception as e:
                print('failed to insert')
                pprint.pprint(record)
        # if typeid == 597:
        #     pprint.pprint(record)
        #     exit()

    eve_mongo.close()


if __name__ == '__main__':
    main(None)