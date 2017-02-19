from interface.trigger import Trigger


# Runs when a System event happens arg should always be a list where the first object is the hook to notify
class SystemTrigger(Trigger):

    async def notify(self, arg):
        if arg[0] in self._tasks:
            for task in self._tasks[arg[0]]:
                await task(self, self._bot, arg[0], arg)
