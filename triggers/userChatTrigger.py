import re

from interface.trigger import Trigger


# A notification system that runs tasks when commands have been requested by the user
class UserChatTrigger(Trigger):

    def __init__(self, bot, command):
        self.command = command
        super().__init__(bot)

    async def notify(self, arg):
        if not arg.content.startswith(self.command):
            return

        arg.content = re.sub(self.command + ' ', '', arg.content, count=1)
        command = arg.content.split(' ')
        sender = arg.author

        if len(command) < 1 or command[0] == '':
            await self._bot.send_message(arg.channel, sender.mention + ', please use ' + self.command + '" help" for a list of commads')
        else:
            if command[0] in self._tasks:
                for task in self._tasks[command[0]]:
                    arg.content = re.sub(command[0] + ' ', '', arg.content, count=1)
                    await task(self, self._bot, command[0], arg)
