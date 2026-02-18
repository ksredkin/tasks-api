from bot.handlers.commands import commands_router
from bot.handlers.callback import callback_router
from bot.handlers.messages import messages_router
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, InputProfilePhotoStatic, FSInputFile
from bot.utils.env_config import EnvConfig
from bot.utils.logger import Logger
import asyncio

logger = Logger(__name__).get_logger()

bot_photo_path = "./bot/images/bot_photo.jpeg"

bot_commands = [
    BotCommand(command="start", description="👋 Приветствие"),
    BotCommand(command="login", description="🔑 Войти в аккаунт"),
    BotCommand(command="register", description="🔒️ Создать аккаунт и войти"),
    BotCommand(command="logout", description="🚫 Выйти из аккаунта"),
    BotCommand(command="tasks", description="📃 Все задачи"),
    BotCommand(command="done", description="📜 Выполненные задачи"),
    BotCommand(command="create_task", description="📝 Создать задачу"),
    BotCommand(command="import_tasks", description="🚀 Импортировать задачи"),
    BotCommand(command="create_folder", description="📁 Создать папку"),
    BotCommand(command="update_folder", description="🔄 Обновить папку"),
    BotCommand(command="delete_folder", description="🚫 Удалить папку"),
    BotCommand(command="help", description="❓️ Справка")
    ]

async def configure_bot(bot: Bot):
    await bot.set_my_commands(bot_commands)
    photo = InputProfilePhotoStatic(photo=FSInputFile(bot_photo_path))
    await bot.set_my_profile_photo(photo=photo)
    await bot.session.close()

async def configure_dp(dp: Dispatcher):
    dp.include_router(commands_router)
    dp.include_router(callback_router)
    dp.include_router(messages_router)

async def start_telegram_bot():
    config = EnvConfig()
    bot = Bot(config.get_token())
    dp = Dispatcher()

    from bot.utils.auth_storage import AuthStorage
    storage = AuthStorage()

    await configure_bot(bot)
    await configure_dp(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_telegram_bot())