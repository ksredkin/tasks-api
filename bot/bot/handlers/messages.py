from bot.keyboards.inline import get_skip_keyboard, get_cancell_keyboard, get_skip_task_text_keyboard, get_choose_folder_keyboard, get_create_choose_folder_keyboard, get_update_skip_folder_keyboard, get_update_task_choose_folder_keyboard, get_import_choose_folder_keyboard, get_create_skip_due_date_keyboard, get_create_skip_visible_from_keyboard, get_update_skip_due_date_keyboard, get_update_skip_visible_from_keyboard, create_inline_keyboard, create_cancell_inline_keyboard
from bot.utils.helpers import finish_task_creation, finish_login, finish_register, finish_task_updation
from bot.messages.auth import no_auth_error, enter_password_message, create_password_message, many_attempts_error
from bot.messages.tasks import enter_task_text, enter_new_task_text, enter_due_date, enter_due_date_error, enter_visible_from
from bot.messages.common import incorrect_day_of_week, incorrect_month_day
from bot.states.user_states import UserLogin, UserRegister
from bot.states.task_states import TaskCreate, TaskUpdate, TaskImport
from bot.messages.folders import choose_folder_message, choose_new_folder_message, choose_folder_for_import
from bot.states.folder_states import FolderCreate, FolderUpdate
from bot.utils.auth_storage import AuthStorage
from bot.utils.api_client import APIClient
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram import types
from datetime import datetime, timezone
import calendar
from bot.utils.attempts_storage import AttemptsStorage
from bot.core.config import MAX_LOGIN_ATTEMPTS
from bot.states.data_states import DataImport
from aiogram import F

messages_router = Router()

@messages_router.message(TaskCreate.waiting_for_recurrence_day_of_week)
async def create_task_process_recurrence_day_of_week(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return
    
    if int(message.text) < 1 or int(message.text) > 7:
        await message.answer(incorrect_day_of_week, parse_mode="html")
        return

    await state.update_data(recurrence_day_of_week=int(message.text)-1)
    await state.set_state(TaskCreate.waiting_for_due_date)
    await message.answer(enter_due_date, reply_markup=get_create_skip_due_date_keyboard())

@messages_router.message(TaskCreate.waiting_for_recurrence_month_day)
async def create_task_process_recurrence_month_day(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return
    
    now = datetime.now(timezone.utc)
    last_day = calendar.monthrange(now.year, now.month)[1]

    if int(message.text) < 1 or int(message.text) > last_day:
        await message.answer(incorrect_month_day, parse_mode="html")
        return

    await state.update_data(recurrence_month_day=int(message.text)-1)
    await state.set_state(TaskCreate.waiting_for_due_date)
    await message.answer(enter_due_date, reply_markup=get_create_skip_due_date_keyboard())

@messages_router.message(TaskCreate.waiting_for_due_date)
async def create_task_process_due_date(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return
    
    try:
        due_date = datetime.strptime(message.text, "%d.%m.%y")
    except Exception:
        await message.answer(enter_due_date_error, parse_mode="html")
        return

    await state.update_data(due_date=due_date)
    await state.set_state(TaskCreate.waiting_for_visible_from)
    await message.answer(enter_visible_from, reply_markup=get_create_skip_visible_from_keyboard())

@messages_router.message(TaskCreate.waiting_for_visible_from)
async def create_task_process_visible_from(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return
    
    try:
        visible_from = datetime.strptime(message.text, "%d.%m.%y")
    except Exception:
        await message.answer(enter_due_date_error, parse_mode="html")
        return

    await state.update_data(visible_from=visible_from)
    await finish_task_creation(message.bot, message.chat.id, message.from_user.id, state)

@messages_router.message(TaskUpdate.waiting_for_recurrence_day_of_week)
async def update_task_process_recurrence_day_of_week(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return
    
    if int(message.text) < 1 or int(message.text) > 7:
        await message.answer(incorrect_day_of_week, parse_mode="html")
        return

    await state.update_data(recurrence_day_of_week=int(message.text)-1)
    await state.set_state(TaskUpdate.waiting_for_due_date)
    await message.answer(enter_due_date, reply_markup=get_update_skip_due_date_keyboard())

@messages_router.message(TaskUpdate.waiting_for_recurrence_month_day)
async def updates_task_process_recurrence_month_day(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return
    
    now = datetime.now(timezone.utc)
    last_day = calendar.monthrange(now.year, now.month)[1]

    if int(message.text) < 1 or int(message.text) > last_day:
        await message.answer(incorrect_month_day, parse_mode="html")
        return

    await state.update_data(recurrence_month_day=int(message.text)-1)
    await state.set_state(TaskUpdate.waiting_for_due_date)
    await message.answer(enter_due_date, reply_markup=get_create_skip_due_date_keyboard())

@messages_router.message(TaskCreate.waiting_for_name)
async def process_task_name(message: types.Message, state: FSMContext):
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
async def process_task_text(message: types.Message, state: FSMContext):
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
async def process_task_text(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return
    
    await state.update_data(text=message.text)
    await finish_task_creation(message.bot, message.chat.id, message.from_user.id, state)
    
@messages_router.message(UserLogin.waiting_for_login)
async def process_login_login(message: types.Message, state: FSMContext):
    if AttemptsStorage().get_attempts(message.from_user.id, message.text) > MAX_LOGIN_ATTEMPTS:
        await message.answer(many_attempts_error, parse_mode="html")
        await state.clear()
        return

    await state.update_data(login=message.text)
    await state.set_state(UserLogin.waiting_for_password)
    await message.answer(enter_password_message, reply_markup=get_cancell_keyboard())

@messages_router.message(UserLogin.waiting_for_password)
async def process_login_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.delete()
    await finish_login(message, state)

@messages_router.message(UserRegister.waiting_for_login)
async def process_register_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await state.set_state(UserRegister.waiting_for_password)
    await message.answer(create_password_message, reply_markup=get_cancell_keyboard())

@messages_router.message(UserRegister.waiting_for_password)
async def process_register_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.delete()
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
async def process_task_update_text(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return
    
    folders = await APIClient.get_user_folders(AuthStorage().get_token(message.from_user.id))

    await state.update_data(text=message.text)
    await state.set_state(TaskUpdate.waiting_for_folder)
    await message.answer(choose_folder_message, reply_markup=get_update_task_choose_folder_keyboard(folders))

@messages_router.message(TaskUpdate.waiting_for_due_date)
async def update_task_process_due_date(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return
    
    try:
        due_date = datetime.strptime(message.text, "%d.%m.%y")
    except Exception:
        await message.answer(enter_due_date_error, parse_mode="html")
        return

    await state.update_data(due_date=due_date)
    await state.set_state(TaskUpdate.waiting_for_visible_from)
    await message.answer(enter_visible_from, reply_markup=get_update_skip_visible_from_keyboard())

@messages_router.message(TaskUpdate.waiting_for_visible_from)
async def update_task_process_visible_from(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return
    
    try:
        visible_from = datetime.strptime(message.text, "%d.%m.%y")
    except Exception:
        await message.answer(enter_due_date_error, parse_mode="html")
        return

    await state.update_data(visible_from=visible_from)
    await finish_task_updation(message.bot, message.chat.id, message.from_user.id, state)

@messages_router.message(DataImport.waiting_for_data, F.document)
async def import_data(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return
    
    buttons = {"🗑️ Заменить всё (старые данные будут удалены)": "import_data_choose_type:delete",
               "➕ Добавить к существующим (дубликаты)": "import_data_choose_type:create",
               "🔄 Обновить только новые (без дубликатов)": "import_data_choose_type:update"
    }

    file = await message.bot.download(message.document)
    await state.update_data(file=file)
    await state.set_state(DataImport.waiting_for_import_type)
    await message.answer("🧭 Как обработать существующие задачи и папки?", reply_markup=create_cancell_inline_keyboard(buttons))