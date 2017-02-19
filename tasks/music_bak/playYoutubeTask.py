import re

from interface.task import Task


class PlayYoutubeTask(Task):

    async def run(self, bot, arg):
        arg[0].content = re.sub(self.hook + ' ', '', arg[0].content, count=1)
        command = arg[0].content.split(' ')

        # if len(command) < 1:
        #    await bot.send_message(arg[0].channels, arg[0].author.mention + self.hook + ' <youtube_url>')
        # else:
        if command[0] != '':
            if arg[1].player is not None and not arg[1].player.is_done():
                await bot.send_message(arg[0].channel, arg[0].author.mention + ' I am currently playing a song at the moment, your request will have to wait')
            else:
                arg[1].player = await bot.voice_client_in(arg[0].server).create_ytdl_player(command[0])
                arg[1].player.start()
