import discord
import asyncio

import key
from bot import Bot

def main():
    bot = Bot()
    bot.run(key.auth_key)

if __name__ == "__main__":
    key.initialize_globals()
    main()
