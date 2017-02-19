from interface.task import Task


# A task that execute python code
class HelpTask(Task):

    async def run(self, bot, arg):
        await bot.send_message(arg.channel, arg.content)
