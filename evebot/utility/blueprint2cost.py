#!/usr/bin/python3

import argparse

from .. import config
from ..connectors import evemongo


def main(args):

    items = evemongo.EveMongo(config.MONGOITEMS)
    blueprint = evemongo.EveMongo(config.MONGOBLUEPRINTS)
    market = evemongo.EveMongo(config.MONGOMARKET)

    request = {'name': args['blueprint']}
    item_record = item.collection.find_one(request)
    item_id = item_record['typeid']
    blueprint_request = {'itemid': item_id}
    blueprint_record = blueprint.collection.find_one(blueprint_request)
    #something about matreials
    #something about finding price
    #dont care anymore


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argrgument('blueprint')
    PARSER.add_argrgument('-e','--efficiency', default=0)
    PARSER.add_argrgument('-q', '--quantity', default=1)
    ARGS = vars(PARSER.parse_args())
    main(ARGS)
