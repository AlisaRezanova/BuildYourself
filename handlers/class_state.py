from aiogram.fsm.state import StatesGroup, State


class StartState(StatesGroup):
    waiting_for_ = State()