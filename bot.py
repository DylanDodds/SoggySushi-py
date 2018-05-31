import discord

# from tasks import voice
# from tasks import music
from tasks import system
from tasks import operation

from triggers.adminChatTrigger import AdminChatTrigger
from triggers.musicChatTrigger import MusicChatTrigger
from triggers.userChatTrigger import UserChatTrigger
from triggers.systemTrigger import SystemTrigger
from chat_engine.chatEngine import ChatEngine

class Bot(discord.Client):

    def __init__(self):
        super().__init__()
        self.chat_triggers = []
        self.systemTrigger = SystemTrigger(self)
        self.register_triggers()
        self.chat_engine = ChatEngine()

    def register_triggers(self):
        act = AdminChatTrigger(self, '--s')
        uct = UserChatTrigger(self, '.s')
        mct = MusicChatTrigger(self, '.m')

        # act.register(voice.join_channel, 'jump')
        # act.register(voice.join_channel, 'join')
        act.register(operation.run_code, 'exec')
        act.register(operation.print_help, 'help')

        # uct.register(voice.join_channel, 'jump')
        # uct.register(voice.join_channel, 'join')
        # uct.register(operation.print_help, 'help')

        # mct.register(music.play_youtube, 'play')
        # mct.register(music.resume, 'play')
        # mct.register(music.stop, 'stop')
        # mct.register(music.pause, 'pause')
        # mct.register(music.volume, 'volume')
        # mct.register(operation.print_help, 'help')

        #self.systemTrigger.register(system.load_libraries, 'on_ready')
        self.systemTrigger.register(system.print_bot_info, 'on_ready')

        self.chat_triggers.extend([act, uct, mct])


    async def on_ready(self):
        notification = ['on_ready']
        await self.systemTrigger.notify(notification)

    async def on_message(self, message):
        # Talking to yourself is the first sign of insanity
        if message.author.id == self.user.id:
            return

        message.content += ' '

        # handle bot training
        if message.channel.id == '451477521834180628':
            print(message.content)
            return

        # Handle private message
        if message.channel.is_private:
            # self.chat_engine.process_message(message)
            return

        for trigger in self.chat_triggers:
            await trigger.notify(message)