import discord
import asyncio

from task import Task
from trigger import Trigger


class Bot(discord.Client):

    def __init__(self):
        super().__init__()
        self._userCmdTrigger = Trigger()
        self._adminCmdTrigger = Trigger()
        self.register_commands()
    
    def register_commands(self):
        pass

    async def on_ready(self):
        print('Soggy Sushi has successfully connected!')
        print('Username: ' + self.user.name)
        print('UserId: ' + self.user.id)

    async def on_message(self, message):
        command = message.content.split(' ')
        sender = message.author

        if message.content.startswith('--s'):
            self._adminCmdTrigger.notify(message)
        elif message.content.startswith('.s'):
            self._userCmdTrigger.notify(message)
            
        if 'pizza' in message.content.lower():
            await self.send_message(message.channel, 'That is the single most pop punk thing you have ever said in your entire life, ever.')
            
        if command[0] == '--s':
            if not sender.top_role.permissions.administrator:
                await self.send_message(message.channel, 'Sorry, ' + sender.mention + ' you do not have permission to do this.')
                return
            if len(command) <= 1:
                await self.send_message(message.channel, sender.mention + ', please use "--s help" for a list of commands')
                return
            if command[1] == 'hop':
                if sender.voice.voice_channel is None:
                    if self.voice_client_in(message.server) is not None:
                        await self.voice_client_in(message.server).disconnect()
                    return
                elif self.is_voice_connected(message.server):
                    await self.voice_client_in(message.server).move_to(sender.voice.voice_channel)
                else:
                    await self.join_voice_channel(sender.voice.voice_channel)
                return
