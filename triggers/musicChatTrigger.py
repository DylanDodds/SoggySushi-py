import re

from interface.trigger import Trigger


# Tasks in this class (other then help) take an arg list consisting of the usual argument
# Passed from the input message, and the current instance of this class for player controls
class MusicChatTrigger(Trigger):

    def __init__(self, bot, command):
        self.command = command
        self.player = None
        super().__init__(bot)

    async def notify(self, arg):
        if not arg.content.startswith(self.command):
            return

        arg.content = re.sub(self.command + ' ', '', arg.content, count=1)
        command = arg.content.split(' ')
        sender = arg.author

        if len(command) < 1 or command[0] == '':
            await self._bot.send_message(arg.channel, sender.mention + ', please use "music help" for a list of commands')
            return

        args = arg
        if command[0] == 'help':
            arg.content = self._command_list_string

        if command[0] != 'help':
            args = [arg, self]

        for task in self._tasks:
            if task.hook == command[0]:
                await task.run(self._bot, args)
