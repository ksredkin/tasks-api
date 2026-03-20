from bot.handlers.commands import commands_router
from bot.handlers.callback import callback_router
from bot.handlers.messages import messages_router
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, InputProfilePhotoStatic, FSInputFile
from bot.utils.env_config import EnvConfig
from bot.utils.logger import Logger
import asyncio
from bot.services.update_tasks_service import update_tasks_service
from bot.core.config import BOT_PHOTO_PATH, BOT_NAME, BOT_DESCRIPTION, BOT_PROFILE_DESCRIPTION, TEMP_FILES_PATH
from aiogram.client.session.aiohttp import AiohttpSession

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
    config = EnvConfig()
    if proxy_address := config.get_proxy_address():
        session = AiohttpSession(proxy=proxy_address)
        bot = Bot(config.get_token(), session=session)
    else:
        bot = Bot(config.get_token())

    dp = Dispatcher()

    from bot.utils.auth_storage import AuthStorage
    storage = AuthStorage()

    from bot.utils.temp_files_manager import TempFilesManager
    magaer = TempFilesManager().configure(TEMP_FILES_PATH)

    #await configure_bot(bot)
    await configure_dp(dp)
    await dp.start_polling(bot)

async def start_telegram_bot():
    bot = asyncio.create_task(telegram_bot())
    tasks_service = asyncio.create_task(update_tasks_service())
    await bot
    await tasks_service

if __name__ == "__main__":
    asyncio.run(start_telegram_bot())