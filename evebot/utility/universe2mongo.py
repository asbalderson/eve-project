#!/usr/bin/python3

import os

from .. import config
from ..connectors import evemongo
from ..universe import universe


def main(args):
    eve_universe = universe.Universe(os.path.join(config.SDE_PATH, 'fsd/universe/eve'))
    eve_mongo = evemongo.EveMongo(config.MONGOUNIVERSE)
    for region in eve_universe.regions.keys():
        for const in eve_universe.regions[region].constellations.keys():
            for solar in eve_universe.regions[region].constellations[const].solarsystems.keys():
                record = eve_universe.regions[region].constellations[const].solarsystems[solar].to_dict()
                record['regionID'] = eve_universe.regions[region].id
                record['regionName'] = region
                record['constellationID'] = eve_universe.regions[region].constellations[const].id
                record['constellationName'] = const
                eve_mongo.collection.insert_one(record)

    eve_mongo.close()


if __name__ == '__main__':
    main(None)
