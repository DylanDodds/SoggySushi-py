from interface.trigger import Trigger


# Runs when a System event happens arg should always be a list where the first object is the hook to notify
class SystemTrigger(Trigger):

    async def notify(self, arg):
        for task in self._tasks:
            if task.hook == arg[0]:
                await task.run(self._bot, arg)
