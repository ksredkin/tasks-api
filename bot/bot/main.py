from bot.handlers.commands import commands_router
from bot.handlers.callback import callback_router
from bot.handlers.messages import messages_router
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, InputProfilePhotoStatic, FSInputFile
from bot.utils.logger import Logger
import asyncio
from bot.services.update_tasks_service import update_tasks_service
from bot.core.config import BOT_PHOTO_PATH, BOT_NAME, BOT_DESCRIPTION, BOT_PROFILE_DESCRIPTION, TEMP_FILES_PATH
from aiogram.client.session.aiohttp import AiohttpSession
import os
from aiogram.client.default import DefaultBotProperties
from singbox2proxy import SingBoxProxy
from bot.utils.auth_storage import AuthStorage
from bot.utils.temp_files_manager import TempFilesManager
import sys

logger = Logger(__name__).get_logger()

bot_commands = [
    BotCommand(command="start", description="👋 Приветствие"),
    BotCommand(command="login", description="🔑 Войти в аккаунт"),
    BotCommand(command="register", description="🔒️ Создать аккаунт и войти"),
    BotCommand(command="logout", description="🚫 Выйти из аккаунта"),
    BotCommand(command="tasks", description="📃 Все задачи"),
    BotCommand(command="today", description="📅 Задачи на сегодня"),
    BotCommand(command="done", description="📜 Выполненные задачи"),
    BotCommand(command="create_task", description="📝 Создать задачу"),
    BotCommand(command="import_tasks", description="🚀 Импортировать задачи"),
    BotCommand(command="create_folder", description="📁 Создать папку"),
    BotCommand(command="update_folder", description="🔄 Обновить папку"),
    BotCommand(command="delete_folder", description="🚫 Удалить папку"),
    BotCommand(command="timer", description="⏳️ Создать таймер"),
    BotCommand(command="stats", description="📊 Статистика за все время"),
    BotCommand(command="export_data", description="💾 Экспорт данных"),
    BotCommand(command="import_data", description="📥 Импорт данных"),
    BotCommand(command="folder_tasks_to_text", description="📃 Получить задачи из папки как текст"),
    BotCommand(command="help", description="❓️ Справка")
    ]

async def configure_bot(bot: Bot):
    logger.info("Начата настройка бота.")
    
    try:
        await bot.set_my_name(BOT_NAME)
    except Exception as e: 
        logger.warning(f"Не удалось установить имя бота: {e}")
    
    try:
        await bot.set_my_commands(bot_commands)
    except Exception as e: 
        logger.warning(f"Не удалось установить команды бота: {e}")
    
    try:
        await bot.set_my_description(BOT_DESCRIPTION)
    except Exception as e: 
        logger.warning(f"Не удалось установить стартовое описание бота: {e}")
    
    try:
        await bot.set_my_short_description(BOT_PROFILE_DESCRIPTION)
    except Exception as e: 
        logger.warning(f"Не удалось установить описание бота: {e}")
    
    try:
        photo = InputProfilePhotoStatic(photo=FSInputFile(BOT_PHOTO_PATH))
        await bot.set_my_profile_photo(photo=photo)
    except Exception as e: 
        logger.warning(f"Не удалось установить фото бота: {e}")
    
    logger.info("Настройка бота завершена.")

async def configure_dp(dp: Dispatcher):
    dp.include_router(commands_router)
    dp.include_router(callback_router)
    dp.include_router(messages_router)

async def telegram_bot():
    try:
        properties = DefaultBotProperties(parse_mode="html")

        if os.getenv("PROXY"):    
            logger.info("Запуск с ипользованием proxy")
            session = AiohttpSession(proxy=os.getenv("PROXY"))
            bot = Bot(os.getenv("TOKEN"), session, properties)
            
        elif os.getenv("VLESS_PROXY"):
            logger.info("Запуск с ипользованием VLESS proxy")

            proxy = SingBoxProxy(os.getenv("VLESS_PROXY"))
            proxy.start()

            session = AiohttpSession(proxy=proxy.socks5_proxy_url)
            bot = Bot(os.getenv("TOKEN"), session, properties)
            
        else:
            logger.info("Запуск без proxy")
            bot = Bot(os.getenv("TOKEN"), default=properties)

        dp = Dispatcher()
        storage = AuthStorage()
        files_manager = TempFilesManager().configure(TEMP_FILES_PATH)

        await configure_bot(bot)
        await configure_dp(dp)
        await dp.start_polling(bot)

    except Exception as e:
        logger.critical(f"Работа бота остановлена: {e}")
        sys.exit(1)

async def start_telegram_bot():
    bot = asyncio.create_task(telegram_bot())
    tasks_service = asyncio.create_task(update_tasks_service())
    await bot
    await tasks_service

if __name__ == "__main__":
    asyncio.run(start_telegram_bot())