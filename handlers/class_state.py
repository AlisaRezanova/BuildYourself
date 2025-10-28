from aiogram.fsm.state import StatesGroup, State


class BackState(StatesGroup):
    habit_selection = State()


class FriendsState(StatesGroup):
    waiting_for_invite_code = State()


class HabitsState(StatesGroup):
    waiting_for_input_state = State()
