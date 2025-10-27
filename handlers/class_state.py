from aiogram.fsm.state import StatesGroup, State


class BackState(StatesGroup):
    habit_selection = State()


class FriendsState(StatesGroup):
    waiting_for_invite_code = State()
