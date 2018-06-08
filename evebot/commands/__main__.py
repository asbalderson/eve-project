#!/usr/bin/env python3

import argparse

from . import timeslut
from . import tradeslut
from . import travelslut


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='call a command to test it')
    SUBPARSER = PARSER.add_subparsers(dest='subcmd')
    SUBPARSER.required = True
    TIMESLUT = SUBPARSER.add_parser('timeslut',
                                    help='call the timeslut command')
    TIMESLUT.add_argument('args',
                          nargs='*')
    TRADESLUT = SUBPARSER.add_parser('tradeslut',
                                     help='call the tradeslut command')
    TRADESLUT.add_argument('args',
                           nargs='*')
    TRAVELSLUT = SUBPARSER.add_parser('travelslut',
                                      help='call the travelslut command')
    TRAVELSLUT.add_argument('args',
                            nargs='*')

    ARGS = PARSER.parse_args()
    if 'help' in ARGS.args:
        ARGS.args = ['--help']
    elif 'h' in ARGS.args:
        ARGS.args = ['-h']
    if ARGS.subcmd == 'timeslut':
        THESE_ARGS = timeslut.do_args(ARGS.args)
        print(timeslut.main(THESE_ARGS))
    elif ARGS.subcmd == 'tradeslut':
        THESE_ARGS = tradeslut.do_args(ARGS.args)
        print(tradeslut.main(THESE_ARGS))
    elif ARGS.subcmd == 'travelslut':
        THESE_ARGS = travelslut.do_args(ARGS.args)
        print(travelslut.main(THESE_ARGS['source'],
                              THESE_ARGS['destination'],
                              THESE_ARGS['ignore']))
