#!/usr/bin/python3

import argparse
import asyncio
import datetime
import discord
import shlex
import time

from discord.ext import commands

from . import __version__

from .commands import travelslut
from .commands import timeslut
from .commands import tradeslut
from .utility.discord_argparse import DiscordArgparser
from .utility.my_help import EveBotHelp

BOT = commands.Bot(command_prefix='-',
                   description='Eve utils, -help for help',
                   formatter=EveBotHelp())
TRIES = 1

async def post_to_logs(message):
    log_channel = BOT.get_channel(454876101119049730)
    await BOT.send_message(log_channel, message)


@BOT.event
async def on_ready():
    print('Logged in as')
    print(BOT.user.name)
    print(BOT.user.id)
    await post_to_logs('connected @ version %s' % __version__)
    await BOT.change_presence(game=discord.Game(name='-help | -<command> --help'))
    print('------')
    global TRIES
    TRIES = 1


@BOT.event
async def on_message(message):
    await BOT.process_commands(message)


@BOT.event
async def on_message_edit(before, after):
    if before.content != after.content:
        await BOT.on_message(after)


@BOT.command(name='travelslut', pass_context=True)
async def call_travelslut(ctx):
    await BOT.type()
    parser = DiscordArgparser(bot=BOT,
                              description='Find distance between 2 systems.  '
                                          'Systems with 2 word names need to be'
                                          'wrapped in "quotes".',
                              usage='-travelslut source destination [-i] [-s]')
    parser.add_argument('source', help='System leaving from')
    parser.add_argument('destination', help='Where you are going or '
                                            '"tradehub" for all systems')
    parser.add_argument('-i', '--ignore',
                        help='Systems to ignore.  Can be specified more than once',
                        action='append')
    parser.add_argument('-s', '--security',
                        help='Security preference for route.  '
                             'One of "shortest", "secure", or "insecure" \n'
                             '\t default=shortest',
                        default='shortest')

    raw_args = shlex.split(ctx.message.content)
    args = parser.parse_args(raw_args[1:])
    if parser.message:
        say = '\n'.join(parser.message)
        await BOT.say('```%s```' % say)
    elif args:
        await BOT.say(travelslut.main(args.source,
                                      args.destination,
                                      args.ignore,
                                      security=args.security))


@BOT.command(name='timeslut', pass_context=True)
async def call_timeslut(ctx):
    await BOT.type()
    parser = DiscordArgparser(bot=BOT,
                              description='Calculate timezone differences from eve time',
                              usage='-timeslut time timezone')
    parser.add_argument('time', help='The time to convert, in the format HHMM '
                                     'as military time i.e. 0830, 1545')
    parser.add_argument('timezone', help='Timezone abbreviations, one of: \n%s'
                                         % ', '.join(timeslut.TZ_DICT.keys()),
                        nargs='*')

    raw_args = shlex.split(ctx.message.content)
    args = parser.parse_args(raw_args[1:])
    if parser.message:
        say = '\n'.join(parser.message)
        await BOT.say('```%s```' % say)
    else:
        await BOT.say(timeslut.main(args))


@BOT.command(name='tradeslut', pass_context=True)
async def call_tradeslut(ctx):
    await BOT.type()
    parser = DiscordArgparser(bot=BOT,
                              description='Get Jita prices for items, invintories, and fittings',
                              usage='-tradeslut [-p percent] item | inventory | fitting [--help] for more info')
    parser.add_argument('-p', '--percent',
                        help='Percent of the cost you wish to display, default=100',
                        default=100)
    subparser = parser.add_subparsers(dest='subcmd')
    subparser.required = True
    item = subparser.add_parser('item', bot=BOT,
                                help='Get the current price for one item')
    item.add_argument('name',
                      help='Name of an item to find the price for, wrapped in quotes')
    item.add_argument('quantity',
                      help='Number of the item you are interested in')
    inventory = subparser.add_parser('inventory', bot=BOT,
                                     help='Get sell value for an invintory of items')
    inventory.add_argument('contents',
                           help='inventory of items to sell, as copied from eve.  wraped in quotes')
    fitting = subparser.add_parser('fitting', bot=BOT,
                                   help='Get the buy cost of a fitting in eve')
    fitting.add_argument('contents',
                         help='A fitting to get the buy cost of wrapped in quotes')
    raw_args = shlex.split(ctx.message.content)
    args = parser.parse_args(raw_args[1:])

    if parser.message:
        say = '\n'.join(parser.message)
        await BOT.say('```%s```' % say)
    else:
        await(BOT.say(tradeslut.main(args)))


@BOT.command(hidden=True)
async def version():
    await BOT.say('I am currently running at %s' % __version__)


@BOT.command(pass_context=True)
async def evetime(ctx):
    await BOT.type()

    parser = DiscordArgparser(bot=BOT,
                              description='Get current eve time, or time in your timezone',
                              usage='-evetime [timezone...]')
    parser.add_argument('timezone',
                        help='Timezone to display eve time in, one of \n%s'
                             % ', '.join(timeslut.TZ_DICT.keys()),
                        nargs='*')
    raw_args = shlex.split(ctx.message.content)
    args = parser.parse_args(raw_args[1:])
    if parser.message:
        say = '\n'.join(parser.message)
        await BOT.say('```%s```' % say)
        return

    now = datetime.datetime.utcnow()
    if not args.timezone:
        timestr = timeslut.get_timestring(now)
        await BOT.say('it is currently %s evetime' % (timestr))
    else:
        message = []
        for timezone in args.timezone:
            if timezone.upper() not in timeslut.TZ_DICT.keys():
                await BOT.say('%s is not a valid timezone, see --help' % timezone.upper())
                return
            else:
                difference = int(timeslut.TZ_DICT.get(timezone.upper()))

            message.append(timeslut.convert_time(now, difference, timezone))
        await BOT.say('\n'.join(message))


def run():
    parser = argparse.ArgumentParser(description='run the eve bot')
    parser.add_argument('key', help='key for discord bot')
    args = parser.parse_args()
    global TRIES
    while TRIES < 6:
        try:
            BOT.run(args.key)
        # Yes, this is terrible, but it lets the bot retry to connect
        except Exception:
            time.sleep(TRIES * 3)
            TRIES += 1
