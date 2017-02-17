from trigger import Trigger


class AdminChatTrigger(Trigger):
    
    def notify(self, arg):
        command = arg.content.split(' ')
        sender = arg.author

        if not sender.top_role.permissions.administrator:
            await self.send_message(message.channel, 'Sorry, ' + sender.mention + ' you do not have permission to do this.')
            return
        if len(command) <= 1:
            await self.send_message(message.channel, sender.mention + ', please use "--s help" for a list of commands')
            return
        for task in self._tasks:
            if task.hook == text[1]:
                task.run(arg)

        
