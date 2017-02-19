import discord

async def load_libraries(trigger, bot, hook, message):
    discord.opus.load_opus('libopus-0')

async def print_bot_info(trigger, bot, hook, message):
    print('Soggy Sushi has successfully connected!')
    print('Username: ' + bot.user.name)
    print('UserId: ' + bot.user.id)
