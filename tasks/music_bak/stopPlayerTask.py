import re

from interface.task import Task


class StopPlayerTask(Task):

    async def run(self, bot, arg):
        arg[0].content = re.sub(self.hook + ' ', '', arg[0].content, count=1)

        if arg[1].player is not None and arg[1].player.is_playing():
            arg[1].player.stop()
