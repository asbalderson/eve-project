#!/usr/bin/env python3

import argparse

from . import timeslut
from . import tradeslut
from . import travelslut


def run():
    parser = argparse.ArgumentParser(description='call a command to test it')
    subparser = parser.add_subparsers(dest='subcmd')
    subparser.required = True
    timeparser = subparser.add_parser('timeslut',
                                    help='call the timeslut command')
    timeparser.add_argument('args',
                          nargs='*')
    tradeparser = subparser.add_parser('tradeslut',
                                     help='call the tradeslut command')
    tradeparser.add_argument('args',
                           nargs='*')
    travelparser = subparser.add_parser('travelslut',
                                      help='call the travelslut command')
    travelparser.add_argument('args',
                            nargs='*')

    args = parser.parse_args()
    if 'help' in args.args:
        args.args = ['--help']
    elif 'h' in args.args:
        args.args = ['-h']
    if args.subcmd == 'timeslut':
        these_args = timeslut.do_args(args.args)
        print(timeslut.main(these_args))
    elif args.subcmd == 'tradeslut':
        these_args = tradeslut.do_args(args.args)
        print(tradeslut.main(these_args))
    elif args.subcmd == 'travelslut':
        these_args = travelslut.do_args(args.args)
        print(travelslut.main(these_args['source'],
                              these_args['destination'],
                              these_args['ignore']))


if __name__ == '__main__':
    run()
