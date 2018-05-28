#!/usr/bin/python3

import os
from pymongo import MongoClient

from .. import config
from .. import universe


def main(args):
    #this takes a really long time, like 20 min
    eve_universe = universe.Universe(os.path.join(config.SDE_PATH, 'fsd/universe/eve'))
    #eve_universe = universe.Universe(os.path.join(config.SDE_PATH, 'test'))
    mongo_client = MongoClient('mongodb://%s:27017' % config.MONGO_IP)
    db = mongo_client[config.MONGODB]
    eveverse = db[config.MONGOUNIVERSE]
    print(type(eveverse))
    for region in eve_universe.regions.keys():
        #print('we have a region')
        for const in eve_universe.regions[region].constellations.keys():
            #print('we have a constellation')
            for solar in eve_universe.regions[region].constellations[const].solarsystems.keys():
                #print('we have a solarsystem')
                record = eve_universe.regions[region].constellations[const].solarsystems[solar].to_dict()
                record['regionID'] = eve_universe.regions[region].id
                record['regionName'] = region
                record['constellationID'] = eve_universe.regions[region].constellations[const].id
                record['constellationName'] = const
                #it didnt insert....
                #print(record)
                temp = eveverse.insert_one(record)
                #why is it not there?
                print(temp.acknowledged)
                print(temp.inserted_id)
    mongo_client.close()


if __name__ == '__main__':
    main(None)
