from bot.messages.auth import successful_account_register, user_already_exists, successful_login, invalid_credentials
from bot.messages.tasks import successful_task_update_message, success_task_create
from bot.messages.folders import success_folder_delete, succes_folder_create, succes_folder_update_message
from bot.messages.common import server_error_message
from bot.utils.api_client import APIClient
from bot.utils.auth_storage import AuthStorage
from bot.utils.logger import Logger
from aiogram.fsm.context import FSMContext
from aiogram import types, Bot

logger = Logger(__name__).get_logger()

async def finish_task_creation(bot: Bot, chat_id: int, telegram_id, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    name = data.get("name")
    text = data.get("text", "Описание не задано.")
    folder_id = data.get("folder_id", 0)

    token = AuthStorage().get_token(telegram_id)
    await APIClient.create_task(token, name, text, folder_id)

    folder = await APIClient.get_user_folder_by_id(token, folder_id)
    folder_name = folder.get("name", "Нет папки.")

    message = success_task_create.replace("{name}", name).replace("{text}", text).replace("{folder}", folder_name)

    await bot.send_message(chat_id, message, parse_mode="html")

async def finish_task_import(bot: Bot, state: FSMContext, chat_id: int, user_id: int):
    data = await state.get_data()
    tasks = data.get('tasks', [])
    folder_id = data.get('folder_id')

    token = AuthStorage().get_token(user_id)

    for task in tasks:
        await APIClient.create_task(token, task, "", folder_id)

    await state.clear()

    await bot.send_message(
        chat_id,
        f"Успешно импортировано {len(tasks)} задач!",
        parse_mode="html"
    )

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

    await APIClient.update_task(token, task_id, name, text, task_state, folder)    
    message = successful_task_update_message.replace("{name}", name).replace("{text}", text).replace("{state}", state)
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