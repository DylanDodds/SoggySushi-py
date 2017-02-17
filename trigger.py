class Trigger:
    def __init__(self):
        self._tasks = []

    def notify(self, arg):
        for task in self._tasks:
            task.run(arg)

    def register(self, task):
        self._tasks.append(task)
