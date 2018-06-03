import discord

# from tasks import voice
# from tasks import music

import json

from tasks import system
from tasks import operation
from data.dataAgent import DataAgent
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
        self.data_agent = DataAgent()
        self.chat_engine = ChatEngine()
        self.last_messages = {}
        self.last_parent_ids = {}
        self.scores = {}


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
        # No Private Messages
        if message.channel.is_private:
            return

        # See if the channel topic has settings
        if message.channel.topic:
            channel_ops = self.try_parse_json(message.channel.topic)
            if channel_ops and channel_ops['action'] and channel_ops['source'] and channel_ops['tag']:
                # Handle Conversation Process
                if channel_ops['action'] == 'converse':
                    if message.author.id == self.user.id:
                        return # Talking to yourself is the first sign of insanity

                    self.chat_engine.generate_response(message.content)
                # Handle data collection process
                elif channel_ops['action'] == 'collect':
                    self.collect_message(channel_ops, message)
            elif channel_ops:
                print("Tried to run channel options, but a required option was not set. Be sure that your topic is a json message containing 'action', 'source', and 'tag'.")

        if message.author.id == self.user.id:
            return

        message.content += ' '
        for trigger in self.chat_triggers:
            await trigger.notify(message)


    def collect_message(self, channel_ops, message):
        if len(message.content) >= 3 and message.content[:2] == '++' and message.channel.id in self.last_messages:
            plusies = int(message.content[2:])
            self.scores[message.channel.id] += plusies
            if self.scores[message.channel.id] > 100:
                self.scores[message.channel.id] = 100
            return
        if message.channel.id not in self.last_messages:
            self.last_messages[message.channel.id] = message
            self.last_parent_ids[message.channel.id] = None
            self.scores[message.channel.id] = 1
            return
        if message.author.id == self.last_messages[message.channel.id].author.id:
            self.last_messages[message.channel.id].content += '\n' + message.content
            return

        # Push Last Message Message
        parent_id = None
        if message.channel.id in self.last_parent_ids:
            parent_id = self.last_parent_ids[message.channel.id]
        self.data_agent.push_comment(self.last_messages[message.channel.id].content,
                                     self.scores[message.channel.id],
                                     channel_ops['source'],
                                     self.last_messages[message.channel.id].id,
                                     parent_id,
                                     channel_ops['tag'],
                                     self.last_messages[message.channel.id].author.id)
        self.last_parent_ids[message.channel.id] = self.last_messages[message.channel.id].id
        self.last_messages[message.channel.id] = message
        self.scores[message.channel.id] = 1


    def try_parse_json(self, str):
        try:
            return json.loads(str)
        except:
            return None