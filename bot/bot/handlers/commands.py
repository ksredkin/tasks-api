from bot.messages.auth import no_auth_error, already_in_account_error, already_without_account_error, enter_login_message, create_login_message, successful_account_logout
from bot.keyboards.inline import get_cancell_keyboard, get_folders_and_tasks_list_keyboard, get_delete_choose_folder_keyboard, get_update_choose_folder_keyboard, get_doned_tasks_list_keyboard
from bot.messages.tasks import get_tasks_message, enter_task_name, enter_tasks_for_import
from bot.messages.common import start_message, help_message
from bot.states.user_states import UserLogin, UserRegister
from bot.messages.folders import enter_name_of_new_folder, choose_folder_to_delete_message, choose_folder_to_update_message
from bot.states.folder_states import FolderCreate, FolderDelete, FolderUpdate
from bot.utils.auth_storage import AuthStorage
from bot.states.task_states import TaskCreate, TaskImport
from aiogram import Router, filters, types
from aiogram.fsm.context import FSMContext
from bot.utils.api_client import APIClient
from bot.utils.logger import Logger

logger = Logger(__name__).get_logger()
commands_router = Router()

@commands_router.message(filters.Command("start"))
async def start(message: types.Message):
    await message.answer(start_message)
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /start")

@commands_router.message(filters.Command("help"))
async def help(message: types.Message):
    await message.answer(help_message)
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /help")

@commands_router.message(filters.Command("tasks"))
async def tasks(message: types.Message):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return

    tasks = await APIClient.get_user_tasks_in_folder(AuthStorage().get_token(message.from_user.id), 0)
    folders = await APIClient.get_user_folders_in_folder(AuthStorage().get_token(message.from_user.id), 0)
    await message.answer(get_tasks_message, parse_mode="html", reply_markup=get_folders_and_tasks_list_keyboard(tasks, folders))
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /tasks")

@commands_router.message(filters.Command("done"))
async def doned(message: types.Message):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return

    tasks = await APIClient.get_user_tasks(AuthStorage().get_token(message.from_user.id))
    filtered_tasks = [task for task in tasks if task.get("state") == "Done"]
    await message.answer(get_tasks_message, parse_mode="html", reply_markup=get_doned_tasks_list_keyboard(filtered_tasks))
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /done")

@commands_router.message(filters.Command("import_tasks"))
async def import_tasks(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return

    await state.set_state(TaskImport.waiting_for_tasks)
    await message.answer(enter_tasks_for_import, parse_mode="html", reply_markup=get_cancell_keyboard())
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /import_tasks")

@commands_router.message(filters.Command("create_task"))
async def create_task(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return  

    await state.set_state(TaskCreate.waiting_for_name)
    await message.answer(enter_task_name, reply_markup=get_cancell_keyboard())
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /create_task")

@commands_router.message(filters.Command("create_folder"))
async def create_folder(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return  

    await state.set_state(FolderCreate.waiting_for_name)
    await message.answer(enter_name_of_new_folder, parse_mode="html", reply_markup=get_cancell_keyboard())
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /create_folder")

@commands_router.message(filters.Command("delete_folder"))
async def delete_folder(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return  

    await state.set_state(FolderDelete.waiting_for_folder)
    folders = await APIClient.get_user_folders(AuthStorage().get_token(message.from_user.id))
    await message.answer(choose_folder_to_delete_message, parse_mode="html", reply_markup=get_delete_choose_folder_keyboard(folders))
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /delete_folder")

@commands_router.message(filters.Command("update_folder"))
async def update_folder(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return  

    await state.set_state(FolderUpdate.waiting_for_folder)
    folders = await APIClient.get_user_folders(AuthStorage().get_token(message.from_user.id))
    await message.answer(choose_folder_to_update_message, parse_mode="html", reply_markup=get_update_choose_folder_keyboard(folders))
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /update_folder")

@commands_router.message(filters.Command("login"))
async def login(message: types.Message, state: FSMContext):
    if AuthStorage().get_token(message.from_user.id):
        await message.answer(already_in_account_error, parse_mode="html")
        return

    await state.set_state(UserLogin.waiting_for_login)
    await message.answer(enter_login_message, reply_markup=get_cancell_keyboard())
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /login")

@commands_router.message(filters.Command("register"))
async def register(message: types.Message, state: FSMContext):
    if AuthStorage().get_token(message.from_user.id):
        await message.answer(already_in_account_error, parse_mode="html")
        return

    await state.set_state(UserRegister.waiting_for_login)
    await message.answer(create_login_message, reply_markup=get_cancell_keyboard())
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /register")

@commands_router.message(filters.Command("logout"))
async def logout(message: types.Message):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(already_without_account_error, parse_mode="html")
        return

    AuthStorage().delete_token(message.from_user.id)
    await message.answer(successful_account_logout)
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /logout")