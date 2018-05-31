from bot import Bot
from config import config

def main():
    bot = Bot()
    bot.run(config['discord']['auth_key'])

if __name__ == "__main__":
    main()
