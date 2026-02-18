from bot.main import start_telegram_bot
from bot.utils.logger import Logger
import asyncio

def main():
    try:
        logger = Logger(__name__).get_logger()
        logger.info("Запуск TasksBot..")
        asyncio.run(start_telegram_bot())
        logger.info("Завершение работы TasksBot..")

    except Exception as e:
        logger.critical(f"Не удалось запустить: {e}")
        raise

if __name__ == "__main__":
    main()