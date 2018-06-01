#!/usr/bin/python3

from .. import config
from ..connectors import evemongo

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
                    record[key] = val['en'].lower()
                else:
                    record[key] = val.lower()
            all_records.append(record)

    eve_mongo = evemongo.EveMongo(config.MONGOITEMS)
    for record in all_records:
        try:
            eve_mongo.collection.insert_one(record)
        except Exception as e:
            print('failed to insert %s' % record)
    eve_mongo.close()


if __name__ == '__main__':
    main(None)