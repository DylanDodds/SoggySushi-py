import re

from interface.task import Task


class DebugTask(Task):

    async def run(self, bot, arg):
        arg.content = re.sub(self.hook + ' ', '', arg.content, count=1)
        pass
