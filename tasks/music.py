async def play_youtube(trigger, bot, hook, message):
    command = message.content.split(' ')

    if len(command) < 1 or command[0] != '':
        if trigger.player is not None and not trigger.player.is_done():
            await bot.send_message(message.channel, message.author.mention + ' I am currently playing a song at the moment, your request will have to wait')
        else:
            trigger.player = await bot.voice_client_in(message.server).create_ytdl_player(command[0])
            trigger.player.start()

async def resume(trigger, bot, hook, message):
    if trigger.player is not None and not trigger.player.is_done():
        trigger.player.resume()

async def stop(trigger, bot, hook, message):
    if trigger.player is not None and trigger.player.is_playing():
        trigger.player.stop()

async def pause(trigger, bot, hook, message):
    if trigger.player is not None and trigger.player.is_playing():
        trigger.player.pause()

async def volume(trigger, bot, hook, message):
        command = message.content.split(' ')

        if not message.author.top_role.permissions.administrator:
            await bot.send_message(message.channel, message.author.mention + ', the volume controls are for stream configuration, you may change personal volume by right clicking the bot in voice chat.')
        elif len(command) < 1:
            await bot.send_message(message.channels, message.author.mention + '[volume (0.1 ~ 1.0)]')
        elif float(command[0]) < 0.1 or float(command[0]) > 1.0:
            await bot.send_message(message.channels, message.author.mention + hook + '[volume (0.1 ~ 1.0)]')
        else:
            if trigger.player is not None:
                trigger.player.volume(float(command[0]))
