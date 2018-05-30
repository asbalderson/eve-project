#!/usr/bin/python3

import argparse
import asyncio
import discord
import shlex

from discord.ext import commands

from . import __version__

from .commands import travelslut
from .utility.discord_argparse import DiscordArgparser

BOT = commands.Bot(command_prefix='-', description='Eve utils, -help for help')


@BOT.event
async def on_ready():
    print('Logged in as')
    print(BOT.user.name)
    print(BOT.user.id)
    await BOT.change_presence(game=discord.Game(name='-help | -<command> --help'))
    print('------')


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
                              description='Find distance between 2 systems',
                              usage='-travelslut source destination [-i]')
    parser.add_argument('source', help='System leaving from')
    parser.add_argument('destination', help='Where you are going or '
                                            '"tradehub" for all systems')
    parser.add_argument('-i', '--ignore',
                        help='Systems to ignore',
                        action='append')
    parser.add_argument('-s', '--security',
                        help='Security prefference for route.  '
                             'One of "shortest", "secure", or "insecure" \n'
                             '\t default=shortest')

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


@BOT.command(hidden=True)
async def version():
    await BOT.say('I am currently running at %s' % __version__)


def run():
    parser = argparse.ArgumentParser(description='run the eve bot')
    parser.add_argument('key', help='key for discord bot')
    args = parser.parse_args()
    BOT.run(args.key)
