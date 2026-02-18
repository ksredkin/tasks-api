from bot.keyboards.inline import get_skip_keyboard, get_cancell_keyboard, get_skip_task_text_keyboard, get_choose_folder_keyboard, get_create_choose_folder_keyboard, get_update_skip_folder_keyboard, get_update_task_choose_folder_keyboard, get_import_choose_folder_keyboard
from bot.utils.helpers import finish_task_creation, finish_login, finish_register, finish_task_updation
from bot.messages.auth import no_auth_error, enter_password_message, create_password_message
from bot.messages.tasks import enter_task_text, enter_new_task_text
from bot.states.user_states import UserLogin, UserRegister
from bot.states.task_states import TaskCreate, TaskUpdate, TaskImport
from bot.messages.folders import choose_folder_message, choose_new_folder_message, choose_folder_for_import
from bot.states.folder_states import FolderCreate, FolderUpdate
from bot.utils.auth_storage import AuthStorage
from bot.utils.api_client import APIClient
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram import types

messages_router = Router()

@messages_router.message(TaskCreate.waiting_for_name)
async def process_note_name(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return
    
    await state.update_data(name=message.text)
    await state.set_state(TaskCreate.waiting_for_text)
    await message.answer(enter_task_text, reply_markup=get_skip_keyboard())

@messages_router.message(TaskImport.waiting_for_tasks)
async def process_import_tasks(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return

    task_list = message.text.split("\n")
    await state.update_data(tasks=task_list)

    folders = await APIClient.get_user_folders(AuthStorage().get_token(message.from_user.id))
    keyboard = get_import_choose_folder_keyboard(folders)

    await state.set_state(TaskImport.waiting_for_folder)
    await message.answer(choose_folder_for_import, reply_markup=keyboard)

@messages_router.message(TaskCreate.waiting_for_text)
async def process_note_text(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return
    
    await state.update_data(text=message.text)
    await state.set_state(TaskCreate.waiting_for_folder)
    folders = await APIClient.get_user_folders(AuthStorage().get_token(message.from_user.id))
    await message.answer(choose_folder_message, reply_markup=get_choose_folder_keyboard(folders))

@messages_router.message(FolderCreate.waiting_for_name)
async def process_folder_name(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return
    
    await state.set_state(FolderCreate.waiting_for_parent_folder)
    await state.update_data(name=message.text)
    folders = await APIClient.get_user_folders(AuthStorage().get_token(message.from_user.id))
    await message.answer(choose_folder_message, reply_markup=get_create_choose_folder_keyboard(folders), parse_mode="html")

@messages_router.message(FolderUpdate.waiting_for_name)
async def process_update_folder_name(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return
    
    await state.set_state(FolderUpdate.waiting_for_parent_folder)
    await state.update_data(name=message.text)
    
    folders = await APIClient.get_user_folders(AuthStorage().get_token(message.from_user.id))
    folder = await state.get_data()
    folder_id = folder.get("folder_id")

    for folder in folders:
        if folder.get("id") == folder_id:
            folders.remove(folder)
            break
    
    await message.answer(choose_new_folder_message, reply_markup=get_update_skip_folder_keyboard(folders))

@messages_router.message(TaskCreate.waiting_for_text)
async def process_note_text(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return
    
    await state.update_data(text=message.text)
    await finish_task_creation(message.bot, message.chat.id, message.from_user.id, state)

@messages_router.message(UserLogin.waiting_for_login)
async def process_login_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await state.set_state(UserLogin.waiting_for_password)
    await message.answer(enter_password_message, reply_markup=get_cancell_keyboard())

@messages_router.message(UserLogin.waiting_for_password)
async def process_login_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    await finish_login(message, state)

@messages_router.message(UserRegister.waiting_for_login)
async def process_register_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await state.set_state(UserRegister.waiting_for_password)
    await message.answer(create_password_message, reply_markup=get_cancell_keyboard())

@messages_router.message(UserRegister.waiting_for_password)
async def process_register_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    await finish_register(message, state)

@messages_router.message(TaskUpdate.waiting_for_name)
async def process_task_update_name(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return
    
    await state.update_data(name=message.text)
    await state.set_state(TaskUpdate.waiting_for_text)
    await message.answer(enter_new_task_text, reply_markup=get_skip_task_text_keyboard())

@messages_router.message(TaskUpdate.waiting_for_text)
async def process_task_update_name(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return
    
    folders = await APIClient.get_user_folders(AuthStorage().get_token(message.from_user.id))

    await state.update_data(text=message.text)
    await state.set_state(TaskUpdate.waiting_for_folder)
    await message.answer(choose_folder_message, reply_markup=get_update_task_choose_folder_keyboard(folders))