import re
import discord
import asyncio

from task import Task

# A task that evaluates python code and sends the returns data to the user
class EvalTask(Task):

    async def run(self, bot, arg):
        command = arg.content.split(' ')
        header = command[0] + ' ' + command[1] + ' '
        func = re.sub(header, '', arg.content, count=1)
        retVal = eval(func)
        await bot.send_message(arg.channel, arg.author.mention + 'return: ' + str(retVal)) 
        
