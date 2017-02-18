from trigger import Trigger


#A notification system that runs tasks when commands have been requested by the user
class UserChatTrigger(Trigger):

    async def notify(self, arg):
        command = arg.content.split(' ')
        sender = arg.author
        if len(command) <= 1:
            await self._bot.send_message(arg.channel, sender.mention + ', please use ".s help" for a list of commads')
        else:
            for task in self._tasks:
                if task.hook == command[1]:
                    await task.run(self._bot, arg)
