import re
import discord
import asyncio

from task import Task

# A task that execute python code
class ExecTask(Task):
    
    async def run(self, bot, arg):
        command = arg.content.split(' ')
        header = command[0] + ' ' + command[1] + ' ' 
        func = re.sub(header, '', arg.content, count=1)
        exec(fun)
        await bot.send_message(arg.channel, arg.author.mention + 'Execution completed')

    async def post(self, bot, channel, msg):
        await bot.send_message(channel, msg)
