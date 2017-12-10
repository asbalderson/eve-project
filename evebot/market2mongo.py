#!/usr/bin/python3

import pprint
from pymongo import MongoClient

from evebot.backend import eve_api
from evebot import config

def main(args):
    #the jita region, i dont know the name of it...
    regionid = 10000002
    #jita
    station_id = 60003760
    market_api = eve_api.EveAPI('https://esi.tech.ccp.is/latest')
    resource = 'markets/%s/orders/' % regionid
    args = {
        'order_type': 'sell',
        'page': 1
    }

    market_api.args = args

    content = market_api.getall(resource)

    mongo_client = MongoClient('mongodb://%s:27017' % config.MONGO_IP)
    db = mongo_client[config.MONGODB]
    markettable = db[config.MONGOMARKET]

    markettable.delete_many({})

    for record in content:
        if record.get('location_id') == station_id:
            markettable.insert_one(record)

if __name__ == '__main__':
    main(None)