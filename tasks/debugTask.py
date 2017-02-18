from task import Task


class DebugTask(Task):

    async def run(self, bot, arg):
        player = await bot.voice_client_in(arg.server).create_ytdl_player(arg.content.split(' ')[2])
        player.start()
