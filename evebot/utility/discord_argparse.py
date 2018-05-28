import argparse
import asyncio

class DiscordArgparser(argparse.ArgumentParser):

    message = []

    def __init__(self, bot=None, *args, **kwargs):
        if not bot:
            raise AttributeError('bot required')
        else:
            self.bot = bot
        argparse.ArgumentParser.__init__(self, *args, **kwargs)


    def _print_message(self, message, file=None):
        if message:
            self.message.append(message)


    def exit(self, status=0, message=None):
        self._print_message(message)

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