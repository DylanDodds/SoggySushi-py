import discord
from interface.task import Task


class LoadLibrariesTask(Task):

    async def run(self, bot, arg):
        discord.opus.load_opus('libopus-0')
