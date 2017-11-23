#!/usr/bin/python3

import argparse
import asyncio
import discord

from evebot import travelslut

CLIENT = discord.Client()

@CLIENT.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@CLIENT.event
async def on_message(message):
    content = message.content
    args = args_from_message(content)
    if content.startswith('-usage'):
        await client.send_message(message.channel, usage())
    elif content.startswith('-travelslut'):
        await client.send_typing(message.channel)
        await client.send_message(message.channel, call_travelslut(args))


def args_from_message(message_content):
    arg_list = []
    for arg in message_content.split()[1:]:
        arg_list.append(arg)
    return arg_list


def call_travelslut(args):
    if len(args) < 2:
        return 'not enough args \n %s' % usage
    else:
        source = args[0]
        destination = args[1]
    if len(args) > 2:
        ignore = args[2]
    else:
        ignore = None
    return travelslut.main(source, destination, ignore)


def usage():
    message = """All commands are prefixed with a - and used with -command <arguments>
Commands:
    usage: returns this message.
    travelslut source destination [ignore]: Ignore values are comma seperated
        if the destination field is tradehub then the distance to Jita, Amarr, and
        Dodixi and Reins will be displayed.
    """
    return message

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='run the eve bot')
    PARSER.add_argument('key', help='key for discord bot')
    ARGS = vars(PARSER.parse_args())
    KEY = ARGS['key']
    client.run(KEY)