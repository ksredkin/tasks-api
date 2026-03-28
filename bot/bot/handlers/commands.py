from bot.messages.auth import no_auth_error, already_in_account_error, already_without_account_error, enter_login_message, create_login_message, successful_account_logout, successful_login, invalid_credentials, many_attempts_error
from bot.keyboards.inline import get_cancell_keyboard, get_folders_and_tasks_list_keyboard, get_delete_choose_folder_keyboard, get_update_choose_folder_keyboard, get_doned_tasks_list_keyboard, get_tasks_list_keyboard, create_inline_keyboard, create_cancell_inline_keyboard
from bot.messages.tasks import get_tasks_message, enter_task_name, enter_tasks_for_import, get_done_tasks_message, get_tasks_today_message, get_tasks_today_error
from bot.messages.common import start_message, help_message, create_timer_error, create_timer_message, tasks_stats_message, folder_stats_message
from bot.states.user_states import UserLogin, UserRegister
from bot.messages.folders import enter_name_of_new_folder, choose_folder_to_delete_message, choose_folder_to_update_message
from bot.states.folder_states import FolderCreate, FolderDelete, FolderUpdate, FolderTasksToText
from bot.utils.auth_storage import AuthStorage
from bot.states.task_states import TaskCreate, TaskImport
from aiogram import Router, filters, types
from aiogram.fsm.context import FSMContext
from bot.utils.api_client import APIClient
from bot.utils.logger import Logger
from bot.core.config import BOT_START_PHOTO_PATH, MAX_LOGIN_ATTEMPTS
from aiogram.exceptions import TelegramNetworkError
from bot.utils.photo_cache import set_photo_id, get_photo_id
from bot.utils.helpers import create_timer
from bot.utils.attempts_storage import AttemptsStorage
from bot.utils.helpers import create_reset_user_attempts_timer
from bot.utils.temp_files_manager import TempFilesManager
from datetime import datetime, timezone
from bot.states.data_states import DataImport
from json import dumps

logger = Logger(__name__).get_logger()
commands_router = Router()
start_photo = types.FSInputFile(BOT_START_PHOTO_PATH)

@commands_router.message(filters.Command("start"))
async def start(message: types.Message):
    try:
        if get_photo_id("start") is None:
            message = await message.answer_photo(start_photo, caption=start_message, parse_mode="html")
            set_photo_id("start", message.photo[-1].file_id)
        else:
            await message.answer_photo(get_photo_id("start"), caption=start_message, parse_mode="html")
    except TelegramNetworkError:
        await message.answer(start_message, parse_mode="html")
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /start")

@commands_router.message(filters.Command("stats"))
async def stats(message: types.Message):
    tasks_stats = await APIClient.get_user_tasks_stats(AuthStorage().get_token(message.from_user.id))
    folders_stats = await APIClient.get_user_folders_stats(AuthStorage().get_token(message.from_user.id))
    
    if not tasks_stats:
        await message.answer("❌ Вы еще не создали задач.", parse_mode="html")

    text = tasks_stats_message.replace("{total}", str(tasks_stats.get("total"))).replace("{active}", str(tasks_stats.get("active"))).replace("{done}", str(tasks_stats.get("done"))).replace("{completion_rate}", str(tasks_stats.get("completion_rate")))

    for name, stats in folders_stats.items():
        text += folder_stats_message.replace("{total}", str(stats.get("total"))).replace("{active}", str(stats.get("active"))).replace("{done}", str(stats.get("done"))).replace("{completion_rate}", str(stats.get("completion_rate"))).replace("{name}", str(name))

    await message.answer(text, parse_mode="html")
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /stats")

@commands_router.message(filters.Command("help"))
async def help(message: types.Message):
    await message.answer(help_message, parse_mode="html")
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /help")

@commands_router.message(filters.Command("timer"))
async def timer(message: types.Message):
    if len(message.text.split()) < 3:
        await message.answer(create_timer_error, parse_mode="html")
        return

    try: 
        minutes = int(message.text.split()[1])
    except Exception:
        await message.answer(create_timer_error, parse_mode="html")
        return

    text = " ".join(message.text.split()[2:])
        
    bot_message = await message.answer(create_timer_message.replace("{name}", text).replace("{minutes}", str(minutes*60//60)), parse_mode="html")
    await create_timer(minutes, message.chat.id, message.bot, text=text, message=bot_message)
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /timer")

@commands_router.message(filters.Command("export_data"))
async def export_data(message: types.Message):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return

    tasks = await APIClient.get_user_tasks(AuthStorage().get_token(message.from_user.id))
    folders = await APIClient.get_user_folders(AuthStorage().get_token(message.from_user.id))

    data_to_export = {"tasks": tasks if tasks else [], "folders": folders if folders else []}
    
    temp_file_manager = TempFilesManager()
    temp_file_path = temp_file_manager.create(dumps(data_to_export), "exported_data_{time}_{username}.json", time=datetime.now(timezone.utc).strftime("%d-%m-%y_%H-%M"), username=str(message.from_user.username))

    await message.answer_document(types.FSInputFile(temp_file_path), caption="✅ Все данные успешно экспортированы.")
    temp_file_manager.delete(temp_file_path)
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /export_data")

@commands_router.message(filters.Command("import_data"))
async def import_data(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return

    await state.set_state(DataImport.waiting_for_data)
    await message.answer("🗃️ Отправьте файл для импортирования данных.", reply_markup=get_cancell_keyboard())
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /import_data")

@commands_router.message(filters.Command("tasks"))
async def tasks(message: types.Message):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return

    all_tasks = await APIClient.get_user_tasks_in_folder(AuthStorage().get_token(message.from_user.id), 0) or []
    
    tasks = []
    for task in all_tasks:
        if task.get("state") != "Done":
            tasks.append(task)

    folders = await APIClient.get_user_folders_in_folder(AuthStorage().get_token(message.from_user.id), 0)
    await message.answer(get_tasks_message, parse_mode="html", reply_markup=get_folders_and_tasks_list_keyboard(tasks, folders))
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /tasks")

@commands_router.message(filters.Command("today"))
async def today(message: types.Message):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return

    tasks = await APIClient.get_user_tasks_today(AuthStorage().get_token(message.from_user.id))

    if not tasks or all(task.get("state") == "Done" for task in tasks):
        await message.answer(get_tasks_today_error, parse_mode="html")
        return

    await message.answer(get_tasks_today_message, parse_mode="html", reply_markup=get_tasks_list_keyboard(tasks))
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /today")

@commands_router.message(filters.Command("done"))
async def doned(message: types.Message):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(no_auth_error, parse_mode="html")
        return

    tasks = await APIClient.get_user_tasks(AuthStorage().get_token(message.from_user.id))
    filtered_tasks = [task for task in tasks if task.get("state") == "Done"]
    await message.answer(get_done_tasks_message, parse_mode="html", reply_markup=get_doned_tasks_list_keyboard(filtered_tasks))
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
    
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /login")
    match len(message.text.split()):
        case 1:
            await state.set_state(UserLogin.waiting_for_login)
            await message.answer(enter_login_message, reply_markup=get_cancell_keyboard())
        case 3:
            if AttemptsStorage().get_attempts(message.from_user.id, message.text.split()[1]) > MAX_LOGIN_ATTEMPTS:
                await message.answer(many_attempts_error, parse_mode="html")
                return

            token = await APIClient.login(message.text.split()[1], message.text.split()[2])
            
            if token is None:
                await message.answer(invalid_credentials, parse_mode="html")
                AttemptsStorage().add_attempt(message.from_user.id, message.text.split()[1])
                
                if AttemptsStorage().get_attempts(message.from_user.id, message.text.split()[1]) > MAX_LOGIN_ATTEMPTS:
                    await create_reset_user_attempts_timer(message.from_user.id, message.text.split()[1])
                
                await message.delete()
                return

            AuthStorage().set_token(message.from_user.id, token)
            AttemptsStorage().reset_attempts(message.from_user.id, message.text.split()[1])
            
            logger.info(f"Пользователь {message.from_user.id} успешно вошел в аккаунт: {message.text.split()[1]}")
            await message.answer(successful_login, parse_mode="html")
            await message.delete()

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

@commands_router.message(filters.Command("folder_tasks_to_text"))
async def folder_tasks_to_text(message: types.Message, state: FSMContext):
    if not AuthStorage().get_token(message.from_user.id):
        await message.answer(already_without_account_error, parse_mode="html")
        return

    folders = await APIClient.get_user_folders(AuthStorage().get_token(message.from_user.id))

    if not folders:
        await message.answer("🚫 У вас еще нет папок!")    
        return

    buttons = {f.get("name"): "choose_folder_to_show_tasks_in_text:" + str(f.get("id")) for f in folders}

    await state.set_state(FolderTasksToText.waiting_for_folder)

    await message.answer("📂 Выберите папку:", reply_markup=create_inline_keyboard(buttons))
    logger.info(f"Пользователь @{message.from_user.username} (id: {message.from_user.id}) вызвал команду /folder_tasks_to_text")