import discord
import asyncio

from task import Task


class JumpTask(Task):

    async def run(self, bot, arg):
        sender = arg.author
        if sender.voice.voice_channel is None:
            if bot.voice_client_in(sender.server) is not None:
                await bot.voice_client_in(sender.server).disconnect()
        elif bot.is_voice_connected(sender.server):
            await bot.voice_client_in(sender.server).move_to(sender.voice.voice_channel)
        else:
            await bot.join_voice_channel(sender.voice.voice_channel)
