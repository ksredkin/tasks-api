from aiogram.fsm.state import State, StatesGroup

class TaskCreate(StatesGroup):
    waiting_for_name = State()
    waiting_for_text = State()
    waiting_for_folder = State()
    waiting_for_recurrence_type = State()
    waiting_for_recurrence_day_of_week = State()
    waiting_for_recurrence_month_day = State()
    waiting_for_due_date = State()
    waiting_for_visible_from = State()

class TaskUpdate(StatesGroup):
    waiting_for_name = State()
    waiting_for_text = State()
    waiting_for_folder = State()
    waiting_for_recurrence_type = State()
    waiting_for_recurrence_day_of_week = State()
    waiting_for_recurrence_month_day = State()
    waiting_for_due_date = State()
    waiting_for_visible_from = State()

class TaskImport(StatesGroup):
    waiting_for_tasks = State()
    waiting_for_folder = State()