async def run_code(trigger, bot, hook, message):
    def ret(p_value):
        ret.return_value = p_value
    ret.return_value = None

    exec(message.content)

    if ret.return_value is None:
        await bot.send_message(message.channel, message.author.mention + ' You code has reached the end of its execution.')
    else:
        await bot.send_message(message.channel, str(ret.return_value))

async def print_help(trigger, bot, hook, message):
    await bot.send_message(message.channel, trigger.command_list_string)
