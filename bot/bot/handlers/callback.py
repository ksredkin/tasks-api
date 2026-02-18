from bot.keyboards.inline import get_task_actions_keyboard, get_skip_task_name_keyboard, get_skip_task_text_keyboard, get_folders_and_tasks_list_keyboard, get_choose_folder_keyboard, get_show_progress_choose_keyboard, get_update_skip_name_keyboard, get_update_skip_folder_keyboard, get_update_show_progress_choose_keyboard, get_update_task_choose_folder_keyboard, get_doned_task_actions_keyboard, get_doned_tasks_list_keyboard
from bot.messages.tasks import enter_new_task_name, enter_new_task_text, successful_mark_a_task_as_completed_message, selected_task_message, successful_undone_task_message
from bot.utils.helpers import finish_task_creation, finish_task_updation, finish_creating_folder, finish_deleting_folder, finish_folder_updation, finish_task_import
from bot.messages.folders import choose_folder_message, show_progress_message, enter_new_name_of_folder, choose_new_folder_message, folder_name_with_progress, folder_name_without_progress
from bot.messages.common import successfull_operation_cancelling
from bot.messages.tasks import successful_delete_task_message, get_tasks_message
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

logger = Logger(__name__).get_logger()
callback_router = Router()

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

@callback_router.callback_query(F.data.startswith("task_select:"))
async def select_task(callback: CallbackQuery):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return

    task_id = int(callback.data.split(":")[1])
    task = await APIClient.get_user_task_by_id(AuthStorage().get_token(callback.from_user.id), task_id)
    
    date = datetime.fromisoformat(task.get("date"))
    nice_date = date.strftime("%d.%m.%y %H:%S")

    message = selected_task_message.replace("{task_name}", task.get("name")).replace("{task_text}", task.get("text")).replace("{task_state}", task.get("state")).replace("{task_date}", nice_date)
    await callback.message.edit_text(message, parse_mode="html", reply_markup=get_task_actions_keyboard(task.get("id"), task.get("folder_id")))

@callback_router.callback_query(F.data.startswith("done_task_select:"))
async def select_task(callback: CallbackQuery):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return

    task_id = int(callback.data.split(":")[1])
    task = await APIClient.get_user_task_by_id(AuthStorage().get_token(callback.from_user.id), task_id)
    
    date = datetime.fromisoformat(task.get("date"))
    nice_date = date.strftime("%d.%m.%y %H:%S")

    message = selected_task_message.replace("{task_name}", task.get("name")).replace("{task_text}", task.get("text")).replace("{task_state}", task.get("state")).replace("{task_date}", nice_date)
    await callback.message.edit_text(message, parse_mode="html", reply_markup=get_doned_task_actions_keyboard(task.get("id")))

@callback_router.callback_query(F.data.startswith("folder_select:"))
async def select_folder(callback: CallbackQuery):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return

    folder_id = int(callback.data.split(":")[1])

    all_tasks = await APIClient.get_user_tasks_in_folder(AuthStorage().get_token(callback.from_user.id), folder_id)
    folders = await APIClient.get_user_folders_in_folder(AuthStorage().get_token(callback.from_user.id), folder_id)
    folder = await APIClient.get_user_folder_by_id(AuthStorage().get_token(callback.from_user.id), folder_id)
    
    name = folder.get("name")
    show_progress = folder.get("show_progress")

    tasks = []
    for task in all_tasks:
        if task.get("state") != "Done":
            tasks.append(task)

    parent_id = None
    if name is not None:
        parent_id = folder.get("parent_id") if folder.get("parent_id") is not None else 0

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
    await APIClient.update_task(AuthStorage().get_token(callback.from_user.id), task_id, task_name=task["name"], task_text=task["text"], task_state="Done")
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
async def update_folder_chow_progress(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    show_progress = callback.data.split(":")[1] == "True"
    await state.update_data(show_progress=show_progress)
    await finish_folder_updation(callback.bot, callback.message.chat.id, callback.from_user.id, state)
    await callback.message.delete()

@callback_router.callback_query(F.data.startswith("folder_choose:"))
async def folder_choose(callback: CallbackQuery, state: FSMContext):
    if not AuthStorage().get_token(callback.from_user.id):
        await callback.message.edit_text(no_auth_error, parse_mode="html")
        return
    
    folder_id = int(callback.data.split(":")[1])
    await state.update_data(folder_id=folder_id)
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
    await finish_task_updation(callback.bot, callback.message.chat.id, callback.from_user.id, state)
    await callback.message.delete()