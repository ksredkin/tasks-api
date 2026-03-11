from bot.messages.auth import successful_account_register, user_already_exists, successful_login, invalid_credentials
from bot.messages.tasks import successful_task_update_message, success_task_create, successful_import_tasks
from bot.messages.folders import success_folder_delete, succes_folder_create, succes_folder_update_message
from bot.messages.common import server_error_message
from bot.utils.api_client import APIClient
from bot.utils.auth_storage import AuthStorage
from bot.utils.logger import Logger
from aiogram.fsm.context import FSMContext
from aiogram import types, Bot
import asyncio
from bot.messages.common import create_timer_message
from bot.utils.attempts_storage import AttemptsStorage
from bot.core.config import MINUTES_TO_RESET_USER_ATTEMPTS, MAX_LOGIN_ATTEMPTS
from bot.utils.attempts_storage import AttemptsStorage
from datetime import datetime

logger = Logger(__name__).get_logger()

async def finish_task_creation(bot: Bot, chat_id: int, telegram_id, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    name = data.get("name", "")
    text = data.get("text", "Описание не задано.")
    folder_id = data.get("folder_id", 0)
    recurrence_type = data.get("recurrence_type", None)
    recurrence_day_of_week = data.get("recurrence_day_of_week", None)
    recurrence_month_day = data.get("recurrence_month_day", None)
    due_date = data.get("due_date", None)
    visible_from = data.get("visible_from", None)

    token = AuthStorage().get_token(telegram_id)
    await APIClient.create_task(token, name, text, folder_id, recurrence_type, recurrence_day_of_week, recurrence_month_day, due_date, visible_from)

    message = success_task_create.replace("{name}", name)
    await bot.send_message(chat_id, message, parse_mode="html")

async def finish_task_import(bot: Bot, state: FSMContext, chat_id: int, user_id: int):
    data = await state.get_data()
    tasks = data.get('tasks', [])
    folder_id = data.get('folder_id')

    token = AuthStorage().get_token(user_id)

    for task in tasks:
        await APIClient.create_task(token, task, "", folder_id)

    await state.clear()

    message = successful_import_tasks.replace("{tasks}", len(tasks))
    await bot.send_message(chat_id, message, parse_mode="html")

async def finish_creating_folder(bot: Bot, chat_id: int, telegram_id, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    name = data.get("name")
    parent_id = data.get("parent_id", 0)
    show_progress = data.get("show_progress", False)

    token = AuthStorage().get_token(telegram_id)
    await APIClient.create_folder(token, name, parent_id, show_progress)

    message = succes_folder_create.replace("{name}", name)
    await bot.send_message(chat_id, message, parse_mode="html")

async def finish_deleting_folder(bot: Bot, chat_id: int, telegram_id, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    folder_id = data.get("folder_id")
    token = AuthStorage().get_token(telegram_id)

    folder = await APIClient.delete_folder(token, folder_id)
    message = success_folder_delete.replace("{name}", folder.get("name"))
    await bot.send_message(chat_id, message, parse_mode="html")

async def finish_task_updation(bot: Bot, chat_id: int, telegram_id, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    task_id = data.get("task_id")
    token = AuthStorage().get_token(telegram_id)
    task = await APIClient.get_user_task_by_id(token, task_id)

    name = data.get("name", task["name"])
    text = data.get("text", task["text"])
    task_state = data.get("state", task["state"])
    folder = data.get("folder_id", task["folder_id"])
    recurrence_type = data.get("recurrence_type", None)
    recurrence_day_of_week = data.get("recurrence_day_of_week", None)
    recurrence_month_day = data.get("recurrence_month_day", None)
    due_date = data.get("due_date", None)
    visible_from = data.get("visible_from", None)

    await APIClient.update_task(token, task_id, name, text, task_state, folder, recurrence_type, recurrence_day_of_week, recurrence_month_day, due_date, visible_from)    
    message = successful_task_update_message.replace("{name}", name)
    await bot.send_message(chat_id, message, parse_mode="html")

async def finish_folder_updation(bot: Bot, chat_id: int, telegram_id, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    folder_id = data.get("folder_id")
    token = AuthStorage().get_token(telegram_id)
    folder = await APIClient.get_user_folder_by_id(token, folder_id)

    name = data.get("name", folder.get("name"))
    parent_id = data.get("parent_id", folder.get("parent_id"))
    show_progress = data.get("show_progress", folder.get("show_progress"))

    await APIClient.update_folder(token, folder_id, name, parent_id, show_progress)    
    message = succes_folder_update_message.replace("{name}", name)
    await bot.send_message(chat_id, message, parse_mode="html")

async def finish_login(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    login = data.get("login")
    password = data.get("password")

    token = await APIClient.login(login, password)
    
    if not token:
        await message.answer(invalid_credentials, parse_mode="html")
        AttemptsStorage().add_attempt(message.from_user.id, login)
        
        if AttemptsStorage().get_attempts(message.from_user.id, login) > MAX_LOGIN_ATTEMPTS:
            await create_reset_user_attempts_timer(message.from_user.id, login)
        
        return

    AuthStorage().set_token(message.from_user.id, token)

    logger.info(f"Пользователь {message.from_user.id} успешно вошел в аккаунт: {login}")
    await message.answer(successful_login, parse_mode="html")

async def finish_register(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    login = data.get("login")
    password = data.get("password")

    is_register_success = await APIClient.register(login, password)

    if not is_register_success:
        await message.answer(user_already_exists, parse_mode="html")
        return

    token = await APIClient.login(login, password)

    if not token:
        await message.answer(server_error_message, parse_mode="html")
        return

    AuthStorage().set_token(message.from_user.id, token)

    logger.info(f"Пользователь {message.from_user.id} успешно зарегистрировался и вошел в аккаунт: {login}")
    await message.answer(successful_account_register, parse_mode="html")

async def create_timer(minutes: int, chat_id: int, bot: Bot, message: types.Message, text: str = None):
    time_to_wait = minutes*60
    current_minutes = time_to_wait // 60

    while time_to_wait > 0:
        await asyncio.sleep(1)
        time_to_wait -= 1

        if current_minutes == time_to_wait//60:
            continue
        
        current_minutes = time_to_wait//60
        try:
            await message.edit_text(create_timer_message.replace("{name}", text).replace("{minutes}", str(time_to_wait//60)))
        except Exception:
            continue

    await message.delete()
    await bot.send_message(chat_id, "⌛️ Время таймера вышло: " + text if text else "⌛️ Время таймера вышло: Сообщение не установлено.")

async def create_reset_user_attempts_timer(user_id: int, login: str):
    await asyncio.sleep(MINUTES_TO_RESET_USER_ATTEMPTS)
    AttemptsStorage().reset_attempts(user_id, login)
