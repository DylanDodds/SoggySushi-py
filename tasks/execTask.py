import re
import asyncio
from task import Task


# A task that execute python code
class ExecTask(Task):

    async def run(self, bot, arg):
        arg.content = re.sub(self.hook + ' ', '', arg.content, count=1)

        def ret(p_value):
            ret.return_value = p_value
        ret.return_value = None

        exec(arg.content)

        if ret.return_value is None:
            await bot.send_message(arg.channel, arg.author.mention + ' You code has reached the end of its execution.')
        else:
            await bot.send_message(arg.channel, str(ret.return_value))
