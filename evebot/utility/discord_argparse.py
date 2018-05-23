import argparse
import asyncio

class DiscordArgparser(argparse.ArgumentParser):


    def __init__(self, bot=None, **kwargs):
        if not bot:
            raise AttributeError('bot required')
        else:
            self.bot = bot
        argparse.ArgumentParser.__init__(self, **kwargs)
        super(self, **kwargs)

    async def _print_message(self, message, file=None):
        self.bot.say(message)


if __name__ == '__main__':
    parser = DiscordArgparser(description='testing the thing',
                              usage='-travelslut [-h] [-v] something')
    parser.add_argument('-v', '--verbose',
                        default=False,
                        action='store_true',
                        help='print more')
    parser.add_argument('something',
                        help='does a thing')

    test = parser.parse_args()