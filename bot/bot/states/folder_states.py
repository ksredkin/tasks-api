from aiogram.fsm.state import State, StatesGroup

class FolderCreate(StatesGroup):
    waiting_for_name = State()
    waiting_for_parent_folder = State()
    waiting_for_show_progress = State()

class FolderUpdate(StatesGroup):
    waiting_for_folder = State()
    waiting_for_name = State()
    waiting_for_parent_folder = State()
    waiting_for_show_progress = State()

class FolderDelete(StatesGroup):
    waiting_for_folder = State()