class Trigger:
    def __init__(self, bot):
        self._tasks = {}
        self._bot = bot
        self.command_list_string = ''

    async def notify(self, arg):
        for task in self._tasks.values():
            task(self, self._bot, arg)

    def register(self, task, hook):
        if hook not in self._tasks:
            self._tasks[hook] = []

        self._tasks[hook].append(task)
        self.command_list_string += '\n' + hook
