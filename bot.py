import discord

from triggers.adminChatTrigger import AdminChatTrigger
from triggers.musicChatTrigger import MusicChatTrigger
from triggers.userChatTrigger import UserChatTrigger

from tasks.debugTask import DebugTask
from tasks.execTask import ExecTask
from tasks.helpTask import HelpTask
from tasks.jumpTask import JumpTask

from tasks.music.playYoutubeTask import PlayYoutubeTask
from tasks.music.stopPlayerTask import StopPlayerTask
from tasks.music.pausePlayerTask import PausePlayerTask
from tasks.music.resumePlayerTask import ResumePlayerTask
from tasks.music.volumePlayerTask import VolumePlayerTask


class Bot(discord.Client):

    def __init__(self):
        super().__init__()
        self.triggers = []
        self.register_triggers()

    def register_triggers(self):
        act = AdminChatTrigger(self, '--s')
        uct = UserChatTrigger(self, '.s')
        mct = MusicChatTrigger(self, '.m')

        mct_spcl = MusicChatTrigger(self, '♪')

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

        mct_spcl.register(PlayYoutubeTask('play'))
        mct_spcl.register(ResumePlayerTask('play'))
        mct_spcl.register(StopPlayerTask('stop'))
        mct_spcl.register(PausePlayerTask('pause'))
        mct_spcl.register(VolumePlayerTask('volume'))
        mct_spcl.register(HelpTask('help'))


        self.triggers.extend([act, uct, mct, mct_spcl])

    async def on_ready(self):
        discord.opus.load_opus('libopus-0')
        print('Soggy Sushi has successfully connected!')
        print('Username: ' + self.user.name)
        print('UserId: ' + self.user.id)

    async def on_message(self, message):
        message.content += ' '
        for trigger in self.triggers:
            await trigger.notify(message)

        if 'pizza' in message.content.lower():
            await self.send_message(message.channel, 'That is the single most pop punk thing you have ever said in your entire life, ever.')
