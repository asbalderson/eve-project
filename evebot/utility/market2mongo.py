#!/usr/bin/python3

from ..connectors import eveapi
from ..connectors import evemongo
from .. import config

def main(buyorder=False, sellorder=False):

    if buyorder:
        table = config.MONGOMARKET_BUY
        type = 'buy'
    elif sellorder:
        table = config.MONGOMARKET_SELL
        type = 'sell'
    else:
        raise RuntimeError('require buy or sell type')

    #the jita region, i dont know the name of it...
    regionid = 10000002
    #jita
    station_id = 60003760
    market_api = eveapi.EveAPI('https://esi.tech.ccp.is/latest')
    resource = 'markets/%s/orders/' % regionid
    args = {
        'order_type': type,
        'page': 1
    }

    market_api.args = args

    content = market_api.getall(resource)

    eve_mongo = evemongo.EveMongo(table)

    eve_mongo.collection.delete_many({})

    for record in content:
        if record.get('location_id') == station_id:
            eve_mongo.collection.insert_one(record)

if __name__ == '__main__':
    main()