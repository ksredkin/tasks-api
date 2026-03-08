from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, timezone

def get_import_choose_folder_keyboard(folders: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for folder in folders:
        builder.button(text=f"{folder.get("name")}", callback_data=f"tasks_import_choose_folder:{folder.get("id")}")

    builder.button(text="⏩ Без папки", callback_data="tasks_import_choose_folder:0")
    builder.button(text="🚫 Отмена", callback_data="cancell")

    builder.adjust(1, repeat=True)

    return builder.as_markup()

def get_create_skip_enter_repeat_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="⏩ Не повторять", callback_data="skip_task_create_repeat")
    builder.button(text="🚫 Отмена", callback_data="cancell")

    builder.adjust(1, repeat=True)

    return builder.as_markup()

def get_update_skip_enter_repeat_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="⏩ Не повторять", callback_data="update_task_repeat:0")
    builder.button(text="⏩ Не обновлять", callback_data="update_task_repeat:-1")
    builder.button(text="🚫 Отмена", callback_data="cancell")

    builder.adjust(1, repeat=True)

    return builder.as_markup()

def get_create_choose_recurrence_type_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="⏩ Не повторять", callback_data="create_task_recurrence_type:None")
    builder.button(text="📅 Каждый день", callback_data="create_task_recurrence_type:daily")
    builder.button(text="📆 Каждую неделю", callback_data="create_task_recurrence_type:weekly")
    builder.button(text="🗓️ Каждый месяц", callback_data="create_task_recurrence_type:monthly")
    builder.button(text="🚫 Отмена", callback_data="cancell")

    builder.adjust(1, repeat=True)

    return builder.as_markup()

def get_update_choose_recurrence_type_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="⏩ Не обновлять", callback_data="update_task_recurrence_type:skip")
    builder.button(text="⏩ Не повторять", callback_data="update_task_recurrence_type:None")
    builder.button(text="📅 Каждый день", callback_data="update_task_recurrence_type:daily")
    builder.button(text="📆 Каждую неделю", callback_data="update_task_recurrence_type:weekly")
    builder.button(text="🗓️ Каждый месяц", callback_data="update_task_recurrence_type:monthly")
    builder.button(text="🚫 Отмена", callback_data="cancell")

    builder.adjust(1, repeat=True)

    return builder.as_markup()

def get_task_actions_keyboard(task_id: int, folder_id: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="✅ Готово", callback_data=f"task_done:{task_id}")
    builder.button(text="🔄 Обновить", callback_data=f"task_update:{task_id}")
    builder.button(text="❌ Удалить", callback_data=f"task_delete:{task_id}")
    builder.button(text="⬅️ Назад", callback_data=f"folder_select:{folder_id}")

    builder.adjust(3)

    return builder.as_markup()

def get_today_task_actions_keyboard(task_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="✅ Готово", callback_data=f"task_done:{task_id}")
    builder.button(text="🔄 Обновить", callback_data=f"task_update:{task_id}")
    builder.button(text="❌ Удалить", callback_data=f"task_delete:{task_id}")
    builder.button(text="⬅️ Назад", callback_data=f"today")

    builder.adjust(3)

    return builder.as_markup()

def get_doned_task_actions_keyboard(task_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="↩️ Вернуть", callback_data=f"task_undone:{task_id}")
    builder.button(text="❌ Удалить", callback_data=f"task_delete:{task_id}")
    builder.button(text="⬅️ Назад", callback_data=f"done")

    builder.adjust(3)

    return builder.as_markup()

def get_show_progress_choose_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="✅ Да", callback_data=f"folder_create_show_progress:True")
    builder.button(text="❌ Нет", callback_data=f"folder_create_show_progress:False")
    builder.button(text="🚫 Отмена", callback_data="cancell")

    builder.adjust(1)

    return builder.as_markup()

def get_update_show_progress_choose_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="✅ Да", callback_data=f"folder_update_show_progress:True")
    builder.button(text="❌ Нет", callback_data=f"folder_update_show_progress:False")
    builder.button(text="🚫 Отмена", callback_data="cancell")

    builder.adjust(1)

    return builder.as_markup()

def get_tasks_list_keyboard(tasks: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for task in tasks:
        if task["state"] == "Done":
            continue

        date = datetime.fromisoformat(task.get("due_date"))
        nice_date = date.strftime("%d.%m.%y")
        builder.button(text=f"{task.get("name")} (сделать до {nice_date if date > datetime.now(timezone.utc) else "❗️просрочено"})", callback_data=f"task_today_select:{task.get("id")}")

    builder.adjust(1, repeat=True)

    return builder.as_markup()

def get_folders_and_tasks_list_keyboard(tasks: list[dict]|None, folders: list[dict]|None, parent_id: int = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if folders is not None:
        for folder in folders:
            builder.button(text=f'Папка "{folder.get("name")}"', callback_data=f"folder_select:{folder.get("id")}")

    if tasks is not None:
        for task in tasks:
            if task.get("due_date") is not None:
                due_date = datetime.fromisoformat(task.get("due_date"))
                nice_date = due_date.strftime("%d.%m.%y")
                message = "(сделать до {due_date})".replace("{due_date}", nice_date) if due_date >= datetime.now(timezone.utc) else "(❗️просрочено)"
            else:
                message = ""
            builder.button(text=f"{task.get("name")} {message}", callback_data=f"task_select:{task.get("id")}")

    if parent_id != None:
        builder.button(text="⬅️ Назад", callback_data=f"folder_select:{parent_id}")

    builder.adjust(1, repeat=True)

    return builder.as_markup()

def get_doned_tasks_list_keyboard(tasks: list[dict]|None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for task in tasks:
        builder.button(text=f"{task.get("name")}", callback_data=f"done_task_select:{task.get("id")}")

    builder.adjust(1, repeat=True)

    return builder.as_markup()

def get_choose_folder_keyboard(folders: list[dict]|None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if folders is not None:
        for folder in folders:
            builder.button(text=f"{folder.get("name")}", callback_data=f"folder_choose:{folder.get("id")}")

    builder.button(text="⏩ Без папки", callback_data="folder_choose:0")
    builder.button(text="🚫 Отмена", callback_data="cancell")

    builder.adjust(1, repeat=True)

    return builder.as_markup()

def get_create_choose_folder_keyboard(folders: list[dict]|None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if folders is not None:
        for folder in folders:
            builder.button(text=f"{folder.get("name")}", callback_data=f"folder_create_choose:{folder.get("id")}")

    builder.button(text=f"🚫 Без папки", callback_data=f"folder_create_choose:0")
    builder.adjust(1, repeat=True)

    return builder.as_markup()

def get_delete_choose_folder_keyboard(folders: list[dict]|None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if folders is not None:
        for folder in folders:
            builder.button(text=f"{folder.get("name")}", callback_data=f"folder_delete_choose:{folder.get("id")}")

    builder.button(text=f"🚫 Отмена", callback_data=f"cancell")
    builder.adjust(1, repeat=True)

    return builder.as_markup()

def get_update_choose_folder_keyboard(folders: list[dict]|None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if folders is not None:
        for folder in folders:
            builder.button(text=f"{folder.get("name")}", callback_data=f"folder_update_choose:{folder.get("id")}")

    builder.button(text=f"🚫 Отмена", callback_data=f"cancell")
    builder.adjust(1, repeat=True)

    return builder.as_markup()

def get_skip_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⏩️ Пропустить", callback_data="skip_text")
    builder.button(text="🚫 Отмена", callback_data="cancell")
    builder.adjust(1, repeat=True)
    return builder.as_markup()

def get_create_skip_due_date_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⏩️ Пропустить", callback_data="skip_create_due_date")
    builder.button(text="🚫 Отмена", callback_data="cancell")
    builder.adjust(1, repeat=True)
    return builder.as_markup()

def get_update_skip_due_date_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⏩️ Не обновлять", callback_data="skip_update_due_date")
    builder.button(text="🚫 Отмена", callback_data="cancell")
    builder.adjust(1, repeat=True)
    return builder.as_markup()

def get_update_skip_visible_from_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⏩️ Не обновлять", callback_data="skip_update_visible_from")
    builder.button(text="🚫 Отмена", callback_data="cancell")
    builder.adjust(1, repeat=True)
    return builder.as_markup()

def get_create_skip_visible_from_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⏩️ Пропустить", callback_data="skip_create_visible_from")
    builder.button(text="🚫 Отмена", callback_data="cancell")
    builder.adjust(1, repeat=True)
    return builder.as_markup()

def get_cancell_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🚫 Отмена", callback_data="cancell")
    return builder.as_markup()

def get_skip_task_name_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⏩️ Не обновлять", callback_data="skip_task_name")
    builder.button(text="🚫 Отмена", callback_data="cancell")
    builder.adjust(1, repeat=True)
    return builder.as_markup()

def get_skip_task_text_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⏩️ Не обновлять", callback_data="skip_task_text")
    builder.button(text="🚫 Отмена", callback_data="cancell")
    builder.adjust(1, repeat=True)
    return builder.as_markup()

def get_update_skip_name_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⏩️ Не обновлять", callback_data="skip_update_folder_name")
    builder.button(text="🚫 Отмена", callback_data="cancell")
    builder.adjust(1, repeat=True)
    return builder.as_markup()

def get_update_skip_folder_keyboard(folders: list[dict]|None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if folders is not None:
        for folder in folders:
            builder.button(text=f"{folder.get("name")}", callback_data=f"new_folder_update_choose:{folder.get("id")}")

    builder.button(text=f"🚫 Без папки", callback_data=f"new_folder_update_choose:0")
    builder.adjust(1, repeat=True)

    return builder.as_markup()

def get_update_task_choose_folder_keyboard(folders: list[dict]|None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if folders is not None:
        for folder in folders:
            builder.button(text=f"{folder.get("name")}", callback_data=f"update_task_choose_folder:{folder.get("id")}")

    builder.button(text=f"🚫 Без папки", callback_data=f"update_task_choose_folder:0")
    builder.adjust(1, repeat=True)

    return builder.as_markup()