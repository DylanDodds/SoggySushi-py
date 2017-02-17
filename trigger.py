class Trigger:
    def __init__(self, bot):
        self._tasks = []
        self._bot = bot
        
    async def notify(self, arg):
        for task in self._tasks:
            task.run(self._bot, arg)

    def register(self, task):
        self._tasks.append(task)

    def set_tasks(self, taskList):
        self._tasks = taskList 
