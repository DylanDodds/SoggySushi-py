import discord
import asyncio

class Bot(discord.Client):

    @asyncio.coroutine
    def on_ready(self):
        print('Soggy Sushi has successfully connected!')
        print('Username: ' + self.user.name)
        print('UserId: ' + self.user.id)

    @asyncio.coroutine
    def on_message(self, message):
        command = message.content.split(' ')
        sender = message.author

        if 'pizza' in message.content.lower():
            yield from self.send_message(message.channel,
                                         'That is the single most pop punk thing you have ever said in your entire life, ever.', tts=True)
            
        if command[0] == '--s':
            if not sender.top_role.permissions.administrator:
                yield from self.send_message(message.channel, 'Sorry, ' + sender.mention + ' you do not have permission to do this.')
                return
            if len(command) <= 1:
                yield from self.send_message(message.channel, sender.mention + ', please use "--s help" for a list of commands')
                return
            if command[1] == 'online':
                yield from self.send_message(message.channel, 'NUMBER 5 ALIVE! SoggySushi, ONLINE!')
