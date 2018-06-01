#!/usr/bin/env python3

import argparse

from . import universe2mongo
from . import items2mongo
from . import market2mongo
from . import blueprint2mongo


def do_args():
    parser = argparse.ArgumentParser(description='Call commands loading mongo data ')
    subparser = parser.add_subparsers(dest='subcmd')
    subparser.required = True

    subparser.add_parser('universe',
                         help='import universe data to the mongo databse')
    subparser.add_parser('items',
                         help='import item data into the mongo database')
    market = subparser.add_parser('market',
                                  help='import market data into the mongo database')
    group = market.add_mutually_exclusive_group(required=True)
    group.add_argument('-b', '--buyorder',
                        help='import buy orders',
                        action='store_true',
                        default=False)
    group.add_argument('-s', '--sellorder',
                        help='import sell orders',
                        action='store_true',
                        default=False)
    subparser.add_parser('blueprint',
                         help='import blueprints into the mongo database')
    return parser.parse_args()


def run():
    args = do_args()
    subcmd = vars(args).pop('subcmd')
    if subcmd == 'universe':
        universe2mongo.main(None)
    elif subcmd == 'items':
        items2mongo.main(None)
    elif subcmd == 'market':
        market2mongo.main(args.buyorder, args.sellorder)
    elif subcmd == 'blueprint':
        blueprint2mongo.main(None)


if __name__ == '__main__':
    run()