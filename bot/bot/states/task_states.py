from aiogram.fsm.state import State, StatesGroup

class TaskCreate(StatesGroup):
    waiting_for_name = State()
    waiting_for_text = State()
    waiting_for_folder = State()

class TaskUpdate(StatesGroup):
    waiting_for_name = State()
    waiting_for_text = State()
    waiting_for_folder = State()

class TaskImport(StatesGroup):
    waiting_for_tasks = State()
    waiting_for_folder = State()