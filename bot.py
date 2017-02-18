import discord
import asyncio

from task import Task
from trigger import Trigger

# Triggers
from triggers.adminChatTrigger import AdminChatTrigger
from triggers.userChatTrigger import UserChatTrigger

# Tasks
from tasks.jumpTask import JumpTask
from tasks.execTask import ExecTask
from tasks.evalTask import EvalTask


class Bot(discord.Client):

    def __init__(self):
        super().__init__()
        self._userCmdTrigger = Trigger(self)
        self._adminCmdTrigger = AdminChatTrigger(self)
        self.register_commands()
    
    async def on_ready(self):
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
        self._adminCmdTrigger.register(ExecTask('exec'))
        self._adminCmdTrigger.register(EvalTask('eval'))

        #User Tasks
        # self._userCmdTrigger.register()
