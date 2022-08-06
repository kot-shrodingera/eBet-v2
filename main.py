from bot.bot import Bot


def main() -> None:
    bot = Bot('./settings.ini')
    bot.run()
    

if __name__ == '__main__':
    main()