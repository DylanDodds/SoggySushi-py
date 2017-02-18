import re
from trigger import Trigger

from triggers.musicChatTrigger import MusicChatTrigger
from tasks.playYoutubeTask import PlayYoutubeTask


# A Notification system that runs tasks when administrative commands have been requested by the user
class AdminChatTrigger(Trigger):

    def __init__(self, bot, command):
        self._musicChatTrigger = MusicChatTrigger(bot, 'music')
        self.register_tasks()
        self.command = command
        super().__init__(bot)

    def register_tasks(self):
        self._musicChatTrigger.register(PlayYoutubeTask('play'))

    async def notify(self, arg):
        if not arg.content.startswith(self.command):
            return

        arg.content = re.sub(self.command + ' ', '', arg.content, count=1)
        command = arg.content.split(' ')
        sender = arg.author

        # Checks that the command's criteria is valid
        if arg.channel.is_private:
            await self._bot.send_message(arg.channel, 'You are not permitted to run admin commands through private channels.')
            return
        if not sender.top_role.permissions.administrator:
            await self._bot.send_message(arg.channel, 'Sorry, ' + sender.mention + ' you do not have permission to do this.')
            return 
        if len(command) < 1:
            await self._bot.send_message(arg.channel, sender.mention + ', please use "' + self.hook + ' help" for a list of commands')
            return

        await self._musicChatTrigger.notify(arg)

        for task in self._tasks:
            if task.hook == command[0]:
                await task.run(self._bot, arg)
