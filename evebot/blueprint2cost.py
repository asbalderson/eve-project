#!/usr/bin/python3

import argparse

from evebot import config
from evebot import eveMongo


def main(args):

    items = eveMongo.EveMongo(config.MONGOITEMS)
    blueprint = eveMongo.EveMongo(config.MONGOBLUEPRINTS)
    market = eveMongo.EveMongo(config.MONGOMARKET)

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
    main(args)
