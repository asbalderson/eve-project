#!/usr/bin/python3

import argparse
import asyncio
import shlex

from discord.ext import commands

from .commands import travelslut
from .utility.discord_argparse import DiscordArgparser

BOT = commands.Bot(command_prefix='-', description='Eve utils, -help for help')


@BOT.event
async def on_ready():
    print('Logged in as')
    print(BOT.user.name)
    print(BOT.user.id)
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

    raw_args = shlex.split(ctx.message.content)
    args = parser.parse_args(raw_args[1:])
    if parser.message:
        await BOT.say('\n'.join(parser.message))
    elif args:
        await BOT.say(travelslut.main(args.source, args.destination, args.ignore))


def run():
    parser = argparse.ArgumentParser(description='run the eve bot')
    parser.add_argument('key', help='key for discord bot')
    args = vars(parser.parse_args())
    BOT.run(args.key)
