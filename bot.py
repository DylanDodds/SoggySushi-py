import discord

from tasks.debugTask import DebugTask

from tasks.chat.execTask import ExecTask
from tasks.chat.helpTask import HelpTask

from tasks.voice.jumpTask import JumpTask

from tasks.music.pausePlayerTask import PausePlayerTask
from tasks.music.playYoutubeTask import PlayYoutubeTask
from tasks.music.resumePlayerTask import ResumePlayerTask
from tasks.music.stopPlayerTask import StopPlayerTask
from tasks.music.volumePlayerTask import VolumePlayerTask

from tasks.system.loadLibrariesTask import LoadLibrariesTask
from tasks.system.printBotInfoTask import PrintBotInfoTask

from triggers.adminChatTrigger import AdminChatTrigger
from triggers.musicChatTrigger import MusicChatTrigger
from triggers.userChatTrigger import UserChatTrigger
from triggers.systemTrigger import SystemTrigger


class Bot(discord.Client):

    def __init__(self):
        super().__init__()
        self.triggers = []
        self.systemTrigger = SystemTrigger(self)
        self.register_triggers()

    def register_triggers(self):
        act = AdminChatTrigger(self, '--s')
        uct = UserChatTrigger(self, '.s')
        mct = MusicChatTrigger(self, '.m')

        act.register(JumpTask('jump'))
        act.register(JumpTask('join'))
        act.register(ExecTask('run'))
        act.register(DebugTask('dbg'))
        act.register(HelpTask('help'))

        uct.register(JumpTask('jump'))
        uct.register(JumpTask('join'))
        uct.register(HelpTask('help'))

        mct.register(PlayYoutubeTask('play'))
        mct.register(ResumePlayerTask('play'))
        mct.register(StopPlayerTask('stop'))
        mct.register(PausePlayerTask('pause'))
        mct.register(VolumePlayerTask('volume'))
        mct.register(HelpTask('help'))

        self.systemTrigger.register(LoadLibrariesTask('on_ready'))
        self.systemTrigger.register(PrintBotInfoTask('on_ready'))

        self.triggers.extend([act, uct, mct])

    async def on_ready(self):
        notification = ['on_ready']
        await self.systemTrigger.notify(notification)

    async def on_message(self, message):
        message.content += ' '
        for trigger in self.triggers:
            await trigger.notify(message)

        if 'pizza' in message.content.lower():
            await self.send_message(message.channel, 'That is the single most pop punk thing you have ever said in your entire life, ever.')
