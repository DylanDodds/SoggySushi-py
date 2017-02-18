class Trigger:
    def __init__(self, bot):
        self._tasks = []
        self._bot = bot
        self._command_list_string = ''

    async def notify(self, arg):
        for task in self._tasks:
            task.run(self._bot, arg)

    def register(self, task):
        self._tasks.append(task)
        self._command_list_string += '\n' + task.hook

    def set_tasks(self, tasklist):
        self._tasks = tasklist
