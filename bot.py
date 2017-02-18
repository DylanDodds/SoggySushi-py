import discord

# Triggers
from triggers.adminChatTrigger import AdminChatTrigger
from triggers.userChatTrigger import UserChatTrigger

# Tasks
from tasks.jumpTask import JumpTask
from tasks.execTask import ExecTask
from tasks.debugTask import DebugTask
from tasks.playYoutubeTask import PlayYoutubeTask

class Bot(discord.Client):

    def __init__(self):
        super().__init__()
        self._userCmdTrigger = UserChatTrigger(self)
        self._adminCmdTrigger = AdminChatTrigger(self)
        self.register_commands()
    
    async def on_ready(self):
        discord.opus.load_opus('libopus-0')
        print('Soggy Sushi has successfully connected!')
        print('Username: ' + self.user.name)
        print('UserId: ' + self.user.id)

    async def on_message(self, message):
        if message.content.startswith('--s'):
            await self._adminCmdTrigger.notify(message)
        elif message.content.startswith('.s'):
            await self._userCmdTrigger.notify(message)     
        elif 'pizza' in message.content.lower():
            await self.send_message(message.channel, 'That is the single most pop punk thing you have ever said in your entire life, ever.')

    def register_commands(self):
        # Admin Tasks
        self._adminCmdTrigger.register(JumpTask('jump'))
        self._adminCmdTrigger.register(ExecTask('run'))
        self._adminCmdTrigger.register(PlayYoutubeTask('music'))
        self._adminCmdTrigger.register(DebugTask('dbg'))

        # User Tasks
        # self._userCmdTrigger.register()
