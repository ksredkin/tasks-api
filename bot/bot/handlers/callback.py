from bot.keyboards.inline import get_task_actions_keyboard, get_skip_task_name_keyboard, get_skip_task_text_keyboard, get_folders_and_tasks_list_keyboard, get_choose_folder_keyboard, get_show_progress_choose_keyboard, get_update_skip_name_keyboard, get_update_skip_folder_keyboard, get_update_show_progress_choose_keyboard, get_update_task_choose_folder_keyboard, get_doned_task_actions_keyboard, get_doned_tasks_list_keyboard, get_create_choose_recurrence_type_keyboard, get_cancell_keyboard, get_update_choose_recurrence_type_keyboard, get_today_task_actions_keyboard, get_tasks_list_keyboard, get_create_skip_due_date_keyboard, get_create_skip_visible_from_keyboard, get_update_skip_due_date_keyboard, create_inline_keyboard
from bot.messages.tasks import enter_new_task_name, enter_new_task_text, successful_mark_a_task_as_completed_message, selected_task_message, successful_undone_task_message, enter_task_recurrence_type, enter_task_recurrence_day_of_week, enter_task_recurrence_month_day, enter_due_date, enter_visible_from
from bot.utils.helpers import finish_task_creation, finish_task_updation, finish_creating_folder, finish_deleting_folder, finish_folder_updation, finish_task_import, finish_import_data, finish_folder_tasks_to_text
from bot.messages.folders import choose_folder_message, show_progress_message, enter_new_name_of_folder, choose_new_folder_message, folder_name_with_progress, folder_name_without_progress
from bot.messages.common import successfull_operation_cancelling
from bot.messages.tasks import successful_delete_task_message, get_tasks_message, get_tasks_today_message, get_tasks_today_error
from bot.states.task_states import TaskCreate, TaskUpdate
from bot.states.folder_states import FolderCreate, FolderUpdate
from bot.utils.auth_storage import AuthStorage
from bot.messages.auth import no_auth_error
from aiogram.fsm.context import FSMContext
from bot.utils.api_client import APIClient
from aiogram.types import CallbackQuery
from bot.utils.logger import Logger
from aiogram import Router, F
from datetime import datetime
import html

logger = Logger(__name__).get_logger()
callback_router = Router()

@callback_router.callback_query(F.data == "skip_create_due_date")
async def create_task_process_due_date(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return

    await state.set_state(TaskCreate.waiting_for_visible_from)
    await callback.message.edit_text(enter_visible_from, reply_markup=get_create_skip_visible_from_keyboard())

@callback_router.callback_query(F.data == "skip_create_visible_from")
async def create_task_process_due_date(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return

    await finish_task_creation(callback.bot, callback.message.chat.id, callback.from_user.id, state)
    await callback.message.delete()

@callback_router.callback_query(F.data == "skip_update_due_date")
async def update_task_process_due_date(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return

    await state.update_data(due_date=-1)
    await state.set_state(TaskUpdate.waiting_for_visible_from)
    await callback.message.edit_text(enter_visible_from, reply_markup=get_create_skip_visible_from_keyboard())

@callback_router.callback_query(F.data == "skip_update_visible_from")
async def update_task_process_due_date(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return

    await state.update_data(visible_from=-1)
    await finish_task_updation(callback.bot, callback.message.chat.id, callback.from_user.id, state)
    await callback.message.delete()

@callback_router.callback_query(F.data.startswith("tasks_import_choose_folder:"))
async def choosing_folder_for_import(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return

    folder_id = int(callback.data.split(":")[1])
    await state.update_data(folder_id=folder_id)

    await finish_task_import(callback.bot, state, callback.message.chat.id, callback.from_user.id)
    await callback.message.delete()

@callback_router.callback_query(F.data == "done")
async def doned(callback: CallbackQuery):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.answer(no_auth_error, parse_mode="html")
        return

    tasks = await APIClient.get_user_tasks(AuthStorage().get_token(callback.from_user.id))
    filtered_tasks = [task for task in tasks if task.get("state") == "Done"]
    await callback.message.edit_text(get_tasks_message, parse_mode="html", reply_markup=get_doned_tasks_list_keyboard(filtered_tasks))

@callback_router.callback_query(F.data.startswith("task_undone:"))
async def undone_task(callback: CallbackQuery):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    task_id = int(callback.data.split(":")[1])
    task = await APIClient.get_user_task_by_id(AuthStorage().get_token(callback.from_user.id), task_id)
    await APIClient.update_task(AuthStorage().get_token(callback.from_user.id), task_id, task.get("name"), task.get("text"), "Active", task.get("folder_id"))
    await callback.message.edit_text(successful_undone_task_message.replace("{name}", task.get("name")), parse_mode="html")

@callback_router.callback_query(F.data.startswith("task_delete:"))
async def delete_task(callback: CallbackQuery):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    task_id = int(callback.data.split(":")[1])
    await APIClient.delete_task(AuthStorage().get_token(callback.from_user.id), task_id)
    await callback.message.edit_text(successful_delete_task_message, parse_mode="html")

@callback_router.callback_query(F.data == "skip_text")
async def skip_text(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return

    await state.set_state(TaskCreate.waiting_for_folder)
    folders = await APIClient.get_user_folders(AuthStorage().get_token(callback.from_user.id))
    await callback.message.edit_text(choose_folder_message, reply_markup=get_choose_folder_keyboard(folders))

@callback_router.callback_query(F.data == "cancell")
async def cancell(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(successfull_operation_cancelling)

@callback_router.callback_query(F.data == "today")
async def today(callback: CallbackQuery):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return

    tasks = await APIClient.get_user_tasks_today(AuthStorage().get_token(callback.from_user.id))
    
    if not tasks:
        await callback.message.edit_text(get_tasks_today_error, parse_mode="html")
        return

    await callback.message.edit_text(get_tasks_today_message, parse_mode="html", reply_markup=get_tasks_list_keyboard(tasks))
    logger.info(f"Пользователь @{callback.from_user.username} (id: {callback.from_user.id}) вызвал команду /today")

@callback_router.callback_query(F.data.startswith("task_today_select:"))
async def select_task(callback: CallbackQuery):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return

    task_id = int(callback.data.split(":")[1])
    task = await APIClient.get_user_task_by_id(AuthStorage().get_token(callback.from_user.id), task_id)
    
    due_date = datetime.fromisoformat(task.get("due_date")).strftime("%d.%m.%y") if task.get("due_date") is not None else "Не задано."
    message = selected_task_message.replace("{task_name}", html.escape(task.get("name"))).replace("{task_text}", html.escape((task.get("text")))).replace("{task_state}", task.get("state")).replace("{task_due_date}", due_date)
    await callback.message.edit_text(message, parse_mode="html", reply_markup=get_today_task_actions_keyboard(task.get("id")))

@callback_router.callback_query(F.data.startswith("task_select:"))
async def select_task(callback: CallbackQuery):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return

    task_id = int(callback.data.split(":")[1])
    task = await APIClient.get_user_task_by_id(AuthStorage().get_token(callback.from_user.id), task_id)
    
    due_date = datetime.fromisoformat(task.get("due_date")).strftime("%d.%m.%y") if task.get("due_date") is not None else "Не задано."

    message = selected_task_message.replace("{task_name}", html.escape(task.get("name"))).replace("{task_text}", html.escape((task.get("text")))).replace("{task_state}", task.get("state")).replace("{task_due_date}", due_date)
    await callback.message.edit_text(message, parse_mode="html", reply_markup=get_task_actions_keyboard(task.get("id"), task.get("folder_id")))

@callback_router.callback_query(F.data.startswith("done_task_select:"))
async def select_done_task(callback: CallbackQuery):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return

    task_id = int(callback.data.split(":")[1])
    task = await APIClient.get_user_task_by_id(AuthStorage().get_token(callback.from_user.id), task_id)
    
    nice_date = datetime.fromisoformat(task.get("due_date")).strftime("%d.%m.%y") if task.get("due_date", None) is not None else "Не задано."
    message = selected_task_message.replace("{task_name}", task.get("name")).replace("{task_text}", html.escape(task.get("text"))).replace("{task_state}", task.get("state")).replace("{task_due_date}", nice_date)
    await callback.message.edit_text(message, parse_mode="html", reply_markup=get_doned_task_actions_keyboard(task.get("id")))

@callback_router.callback_query(F.data.startswith("folder_select:"))
async def select_folder(callback: CallbackQuery):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return

    folder_id = int(callback.data.split(":")[1]) if callback.data.split(":")[1] != "None" else 0

    all_tasks = await APIClient.get_user_tasks_in_folder(AuthStorage().get_token(callback.from_user.id), folder_id)
    folders = await APIClient.get_user_folders_in_folder(AuthStorage().get_token(callback.from_user.id), folder_id)
    folder = await APIClient.get_user_folder_by_id(AuthStorage().get_token(callback.from_user.id), folder_id)

    name = folder.get("name")

    tasks = []
    for task in all_tasks:
        if task.get("state") != "Done":
            tasks.append(task)

    parent_id = None
    if name is not None:
        parent_id = folder.get("parent_id") if folder.get("parent_id") is not None else 0

    show_progress = folder.get("show_progress")

    progress = None
    if show_progress == True:
        api_folder_with_progress = await APIClient.get_folder_progress(AuthStorage().get_token(callback.from_user.id), folder.get("id"))
        progress = api_folder_with_progress.get("progress")

    if name is not None:
        if show_progress == True:
            folder_name = folder_name_with_progress.replace("{name}", name).replace("{progress}", str(progress * 100 if progress is not None else 100))
        else:
            folder_name = folder_name_without_progress.replace("{name}", name)
    else:
        folder_name = get_tasks_message

    await callback.message.edit_text(folder_name, parse_mode="html", reply_markup=get_folders_and_tasks_list_keyboard(tasks, folders, parent_id=parent_id))
    
@callback_router.callback_query(F.data.startswith("task_done:"))
async def task_done(callback: CallbackQuery):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return

    task_id = int(callback.data.split(":")[1])
    
    task = await APIClient.get_user_task_by_id(AuthStorage().get_token(callback.from_user.id), task_id)
    await APIClient.update_task(AuthStorage().get_token(callback.from_user.id), task_id, task_name=task["name"], task_text=task.get("text"), task_state="Done", due_date=task.get("repeat_interval"), visible_from=datetime.fromisoformat(task.get("visible_from")) if task.get("visible_from") is not None else None, folder_id=task.get("folder_id"), recurrence_type=task.get("recurrence_type"), recurrence_day_of_week=task.get("recurrence_day_of_week"), recurrence_month_day=task.get("recurrence_month_day"))
    await callback.message.edit_text(successful_mark_a_task_as_completed_message.replace("{task_name}", task["name"]), parse_mode="html")

@callback_router.callback_query(F.data == "skip_task_text")
async def skip_task_text(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return

    folders = await APIClient.get_user_folders(AuthStorage().get_token(callback.from_user.id))

    await state.set_state(TaskUpdate.waiting_for_folder)
    await callback.message.edit_text(choose_folder_message, reply_markup=get_update_task_choose_folder_keyboard(folders))

@callback_router.callback_query(F.data.startswith("folder_create_choose:"))
async def creating_folder_choose_folder(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    parent_id = int(callback.data.split(":")[1])
    await state.update_data(parent_id=parent_id)
    await state.set_state(FolderCreate.waiting_for_show_progress)
    await callback.message.edit_text(show_progress_message, reply_markup=get_show_progress_choose_keyboard())

@callback_router.callback_query(F.data.startswith("folder_create_show_progress:"), FolderCreate.waiting_for_show_progress)
async def creating_folder(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    show_progress = callback.data.split(":")[1] == "True"
    await state.update_data(show_progress=show_progress)
    await finish_creating_folder(callback.bot, callback.message.chat.id, callback.from_user.id, state)
    await callback.message.delete()

@callback_router.callback_query(F.data.startswith("folder_delete_choose:"))
async def delete_folder(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    folder_id = int(callback.data.split(":")[1])
    await state.update_data(folder_id=folder_id)
    await finish_deleting_folder(callback.bot, callback.message.chat.id, callback.from_user.id, state)
    await callback.message.delete()

@callback_router.callback_query(F.data.startswith("choose_folder_to_show_tasks_in_text:"))
async def folder_tasks_to_text_process_folder(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    folder_id = int(callback.data.split(":")[1])
    await state.update_data(folder_id=folder_id)

    buttons = {"📕 Название": "choose_what_to_show:name",
               "📑 Название и описание": "choose_what_to_show:name_and_text",
               "🗂️ Все данные": "choose_what_to_show:all_data"
               }

    await callback.message.edit_text("🗺️ Что вывести у задач?", reply_markup=create_inline_keyboard(buttons))
    
@callback_router.callback_query(F.data.startswith("choose_what_to_show:"))
async def folder_tasks_to_text_process_what_to_show(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    what_to_show = callback.data.split(":")[1]
    await state.update_data(what_to_show=what_to_show)
    await finish_folder_tasks_to_text(callback.bot, callback.message.chat.id, callback.from_user.id, state)
    await callback.message.delete()

@callback_router.callback_query(F.data.startswith("folder_update_choose:"))
async def update_folder(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    folder_id = int(callback.data.split(":")[1])
    await state.update_data(folder_id=folder_id)
    await state.set_state(FolderUpdate.waiting_for_name)
    await callback.message.edit_text(enter_new_name_of_folder, reply_markup=get_update_skip_name_keyboard(), parse_mode="html")

@callback_router.callback_query(F.data == "skip_update_folder_name")
async def update_folder(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    await state.set_state(FolderUpdate.waiting_for_parent_folder)
    folders = await APIClient.get_user_folders(AuthStorage().get_token(callback.from_user.id))
    
    folder = await state.get_data()
    folder_id = folder.get("folder_id")

    for folder in folders:
        if folder.get("id") == folder_id:
            folders.remove(folder)
            break

    await callback.message.edit_text(choose_new_folder_message, reply_markup=get_update_skip_folder_keyboard(folders))

@callback_router.callback_query(F.data.startswith("new_folder_update_choose:"))
async def update_folder(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    parent_id = int(callback.data.split(":")[1])
    await state.set_state(FolderUpdate.waiting_for_show_progress)
    await state.update_data(parent_id=parent_id)
    await callback.message.edit_text(show_progress_message, reply_markup=get_update_show_progress_choose_keyboard())

@callback_router.callback_query(F.data.startswith("folder_update_show_progress:"))
async def update_folder_show_progress(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    show_progress = callback.data.split(":")[1] == "True"
    await state.update_data(show_progress=show_progress)
    await finish_folder_updation(callback.bot, callback.message.chat.id, callback.from_user.id, state)
    await callback.message.delete()

@callback_router.callback_query(F.data.startswith("update_task_recurrence_type:"))
async def update_task_process_recurrence_type(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    recurrence_type = callback.data.split(":")[1] if callback.data.split(":")[1] != "None" else None
    await state.update_data(recurrence_type=recurrence_type)

    match recurrence_type:
        case "daily":
            await state.set_state(TaskUpdate.waiting_for_due_date)
            await callback.message.edit_text(enter_due_date, reply_markup=get_update_skip_due_date_keyboard())
        case "skip":
            await state.set_state(TaskUpdate.waiting_for_due_date)
            await callback.message.edit_text(enter_due_date, reply_markup=get_update_skip_due_date_keyboard())
        case None:
            await state.set_state(TaskUpdate.waiting_for_due_date)
            await callback.message.edit_text(enter_due_date, reply_markup=get_update_skip_due_date_keyboard())
        case "weekly":
            await state.set_state(TaskUpdate.waiting_for_recurrence_day_of_week)
            await callback.message.edit_text(enter_task_recurrence_day_of_week, reply_markup=get_cancell_keyboard())
        case "monthly":
            await state.set_state(TaskUpdate.waiting_for_recurrence_month_day)
            await callback.message.edit_text(enter_task_recurrence_month_day, reply_markup=get_cancell_keyboard())

@callback_router.callback_query(F.data.startswith("import_data_choose_type:"))
async def import_data_process_type(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    import_type = callback.data.split(":")[1]
    await state.update_data(import_type=import_type)

    buttons = {"✅ Продолжить": "finish_import_data",
               "🚫 Отмена": "cancell"
               }
    keyboard = create_inline_keyboard(buttons)

    await callback.message.edit_text("❓ Вы уверены, что хотите продолжить?", reply_markup=keyboard)

@callback_router.callback_query(F.data == "finish_import_data")
async def process_finish_import_data(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    await finish_import_data(callback.bot, state, callback.message.chat.id, callback.from_user.id)
    await callback.message.delete()

@callback_router.callback_query(F.data.startswith("folder_choose:"))
async def folder_choose(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    folder_id = int(callback.data.split(":")[1])
    await state.update_data(folder_id=folder_id)
    await state.set_state(TaskCreate.waiting_for_recurrence_type)
    await callback.message.edit_text(enter_task_recurrence_type, reply_markup=get_create_choose_recurrence_type_keyboard())

@callback_router.callback_query(F.data.startswith("create_task_recurrence_type:"))
async def create_task_process_recurrence_type(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    recurrence_type = callback.data.split(":")[1] if callback.data.split(":")[1] != "None" else None
    await state.update_data(recurrence_type=recurrence_type)

    match recurrence_type:
        case "daily":
            await state.set_state(TaskCreate.waiting_for_due_date)
            await callback.message.edit_text(enter_due_date, reply_markup=get_create_skip_due_date_keyboard())
        case "skip":
            await state.set_state(TaskCreate.waiting_for_due_date)
            await callback.message.edit_text(enter_due_date, reply_markup=get_create_skip_due_date_keyboard())
        case None:
            await state.set_state(TaskCreate.waiting_for_due_date)
            await callback.message.edit_text(enter_due_date, reply_markup=get_create_skip_due_date_keyboard())
        case "weekly":
            await state.set_state(TaskCreate.waiting_for_recurrence_day_of_week)
            await callback.message.edit_text(enter_task_recurrence_day_of_week, reply_markup=get_cancell_keyboard())
        case "monthly":
            await state.set_state(TaskCreate.waiting_for_recurrence_month_day)
            await callback.message.edit_text(enter_task_recurrence_month_day, reply_markup=get_cancell_keyboard())

@callback_router.callback_query(F.data == "skip_task_create_repeat")
async def folder_choose(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
     
    await finish_task_creation(callback.bot, callback.message.chat.id, callback.from_user.id, state)
    await callback.message.delete()

@callback_router.callback_query(F.data == "skip_task_name")
async def skip_task_name(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    await state.set_state(TaskUpdate.waiting_for_text)
    await callback.message.edit_text(enter_new_task_text, reply_markup=get_skip_task_text_keyboard())

@callback_router.callback_query(F.data.startswith("task_update:"))
async def update_task(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    task_id = int(callback.data.split(":")[1])
    await state.set_state(TaskUpdate.waiting_for_name)
    await state.update_data(task_id=task_id)
    await callback.message.edit_text(enter_new_task_name, reply_markup=get_skip_task_name_keyboard())

@callback_router.callback_query(F.data.startswith("update_task_choose_folder:"))
async def updating_task_choose_folder(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return

    folder_id = int(callback.data.split(":")[1])
    await state.update_data(folder_id=folder_id)
    await state.set_state(TaskUpdate.waiting_for_recurrence_type)
    await callback.message.edit_text(enter_task_recurrence_type, reply_markup=get_update_choose_recurrence_type_keyboard())