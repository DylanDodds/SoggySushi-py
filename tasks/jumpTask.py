import discord
import asyncio

from task import Task


class JumpTask(Task):

    async def run(self, arg):
        sender = arg.author
        if sender.voice.voice_channel is None:
            if self.voice_client_in(sender.server) is not None:
                await self.voice_client_in(sender.server).disconnect()
            return
        elif self.is_voice_connected(sender.server):
            await self.voice_client_in(sender.server).move_to(sender.voice.voice_channel)
        else:
            await self.join_voice_channel(sender.voice.voice_channel)
