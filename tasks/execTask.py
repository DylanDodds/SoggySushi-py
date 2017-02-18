import re
import asyncio
from task import Task


# A task that execute python code
class ExecTask(Task):

    def __init__(self, hook):
        super().__init__(hook)

    async def run(self, bot, arg):
        command = arg.content.split(' ')
        header = command[0] + ' ' + command[1] + ' '
        func = re.sub(header, '', arg.content, count=1).encode('ascii')

        def ret(p_value):
            ret.return_value = p_value
        ret.return_value = None

        exec(func)

        if ret.return_value is None:
            await bot.send_message(arg.channel, arg.author.mention + ' You code has reached the end of its execution.')
        else:
            await bot.send_message(arg.channel, str(ret.return_value))
