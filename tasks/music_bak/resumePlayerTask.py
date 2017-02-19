import re

from interface.task import Task


class ResumePlayerTask(Task):

    async def run(self, bot, arg):
        arg[0].content = re.sub(self.hook + ' ', '', arg[0].content, count=1)

        if arg[1].player is not None and not arg[1].player.is_done():
            arg[1].player.resume()
