from aiogram.fsm.state import State, StatesGroup

class UserLogin(StatesGroup):
    waiting_for_login = State()
    waiting_for_password = State()

class UserRegister(StatesGroup):
    waiting_for_login = State()
    waiting_for_password = State()