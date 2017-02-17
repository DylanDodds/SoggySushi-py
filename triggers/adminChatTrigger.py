from trigger import Trigger


class AdminChatTrigger(Trigger):
    
    async def notify(self, arg):
        command = arg.content.split(' ')
        sender = arg.author
        
        if not sender.top_role.permissions.administrator:
            await self._bot.send_message(arg.channel, 'Sorry, ' + sender.mention + ' you do not have permission to do this.')
            return
        if len(command) <= 1:
            await self._bot.send_message(arg.channel, sender.mention + ', please use "--s help" for a list of commands')
            return
        for task in self._tasks:
            if task.hook == command[1]:
                await task.run(self._bot, arg)
