from aiogram.fsm.state import StatesGroup, State


class Authentication(StatesGroup):
    login = State()
    password = State()