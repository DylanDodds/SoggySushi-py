import re
from task import Task


class VolumePlayerTask(Task):

    async def run(self, bot, arg):
        arg[0].content = re.sub(self.hook + ' ', '', arg[0].content, count=1)
        command = arg[0].content.split(' ')

        if not arg[0].author.top_role.permissions.administrator:
            await bot.send_message(arg[0].channels, arg[0].author.mention + ', the volume controls are for stream configuration, you may change personal volume by right clicking the bot in voice chat.')
        elif len(command) < 1:
            await bot.send_message(arg[0].channels, arg[0].author.mention + self.hook + ' [volume (0.1 ~ 1.0)]')
        elif float(command[0]) < 0.1 or float(command[0]) > 1.0:
            await bot.send_message(arg[0].channels, arg[0].author.mention + self.hook + ' [volume (0.1 ~ 1.0)]')
        else:
            if arg[1].player is not None:
                arg[1].player.volume(float(command[0]))
