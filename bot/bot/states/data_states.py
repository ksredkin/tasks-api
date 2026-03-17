from aiogram.fsm.state import State, StatesGroup

class DataImport(StatesGroup):
    waiting_for_data = State()
    waiting_for_import_type = State()
    waiting_for_confirm = State()