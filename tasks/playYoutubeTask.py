import re
from task import Task


class PlayYoutubeTask(Task):

    async def run(self, bot, arg):
        arg.content = re.sub(self.hook + ' ', '', arg.content, count=1)
        command = arg.content.split(' ')

        if len(command) < 1:
            await bot.send_message(arg.channels, arg.author.mention + ' Usage: --s ' + self.hook + ' <youtube_url>')
        else:
            player = await bot.voice_client_in(arg.server).create_ytdl_player(command[0])
            player.start()
