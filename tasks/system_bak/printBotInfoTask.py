from interface.task import Task


class PrintBotInfoTask(Task):

    async def run(self, bot, arg):
        print('Soggy Sushi has successfully connected!')
        print('Username: ' + bot.user.name)
        print('UserId: ' + bot.user.id)


