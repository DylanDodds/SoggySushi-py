import discord

# Triggers
from triggers.adminChatTrigger import AdminChatTrigger
from triggers.userChatTrigger import UserChatTrigger

# Tasks
from tasks.jumpTask import JumpTask
from tasks.execTask import ExecTask
from tasks.debugTask import DebugTask


class Bot(discord.Client):

    def __init__(self):
        super().__init__()
        self.triggers = []
        self.register_triggers()

    def register_triggers(self):
        act = AdminChatTrigger(self, '--s')
        uct = UserChatTrigger(self, '.s')

        act.register(JumpTask('jump'))
        act.register(ExecTask('run'))
        act.register(DebugTask('dbg'))

        self.triggers.append(act)
        self.triggers.append(uct)

    async def on_ready(self):
        discord.opus.load_opus('libopus-0')
        print('Soggy Sushi has successfully connected!')
        print('Username: ' + self.user.name)
        print('UserId: ' + self.user.id)

    async def on_message(self, message):
        message.content += ' '
        for trigger in self.triggers:
            await trigger.notify(message)

        if 'pizza' in message.content.lower():
            await self.send_message(message.channel, 'That is the single most pop punk thing you have ever said in your entire life, ever.')
