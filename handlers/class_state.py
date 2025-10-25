from aiogram.fsm.state import StatesGroup, State


class BackState(StatesGroup):
    habit_selection = State()
