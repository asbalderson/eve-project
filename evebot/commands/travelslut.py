#!/usr/bin/python3


import argparse

from .. import config
from ..connectors import evemongo
from ..connectors import eveapi


def get_system_id(mongo, system_name):
    request = {'name': system_name.lower()}
    record = mongo.collection.find_one(request)
    assert record, 'System %s not found, check for typo' % system_name
    return record['id']


def get_system_name(mongo, sys_id):
    request = {'id': sys_id}
    record = mongo.collection.find_one(request)
    return '%s %s\n' % (record['name'], record['security'])


def main(source, destination, ignore, verbose=True):
    tradehubs = ['jita', 'amarr', 'dodixie', 'rens']

    eveslut = evemongo.EveMongo(config.MONGOUNIVERSE)
    source_id = get_system_id(eveslut, source)

    if destination == 'tradehub':
        message = ''
        for sys in tradehubs:
            message += main(source, sys, ignore, False)
    else:
        destination_id = get_system_id(eveslut, destination)
        avoidance = []
        if ignore:
            for sys in ignore:
                avoidance.append(str(get_system_id(eveslut, sys)))

        eveapi = eveapi.EveAPI('https://esi.tech.ccp.is/latest')
        if len(avoidance) > 0:
            tmp = '%2C'.join(avoidance)
            eveapi.args = {'avoid': tmp}
        eveapi.args = {'flag': 'shortest'}
        # eventually add a security/saftey
        resource = 'route/%s/%s' % (source_id, destination_id)
        journey_list = eveapi.try_request(resource)
        if type(journey_list) == dict:
            return 'Error, %s' % journey_list['error']
        message = '%s to %s is %s jumps:\n' % (source, destination, str(len(journey_list) -1))

        if verbose:
            for sys_id in journey_list:
                message = message + get_system_name(eveslut, sys_id)

    return message


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='what the??')
    PARSER.add_argument('source', help='system leaving from')
    PARSER.add_argument('destination', help='where you are going', default='trade')
    PARSER.add_argument('-i', '--ignore', help='systems to ignore, comma seperated')
    #need someting for safety
    ARGS = vars(PARSER.parse_args())
    print(main(ARGS['source'], ARGS['destination'], ARGS['ignore']))
