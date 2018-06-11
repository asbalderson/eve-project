from discord.ext.commands import formatter


class EveBotHelp(formatter.HelpFormatter):

    def __init__(self, *args, **kwags):
        formatter.HelpFormatter.__init__(self, *args, **kwags)

    def get_ending_note(self):
        return 'Type command --help or command -h for more info ' \
               'on a command.'
