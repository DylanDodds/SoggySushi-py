import re
from trigger import Trigger


class MusicChatTrigger(Trigger):

    def __init__(self, bot, command):
        self.command = command
        super().__init__(bot)

    async def notify(self, arg):
        if not arg.content.startswith(self.command):
            return

        arg.content = re.sub(self.command + ' ', '', arg.content, count=1)

        command = arg.content.split(' ')
        sender = arg.author

        if len(command) < 1 and not self._command_list_string.contains(command[0]):
            await self._bot.send_message(arg.channel, sender.mention + ', please use "music help" for a list of commands')
            return

        if command[0] == 'help':
            arg.content = self._command_list_string

        for task in self._tasks:
            if task.hook == command[0]:
                await task.run(self._bot, arg)
