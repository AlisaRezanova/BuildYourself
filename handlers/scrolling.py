from aiogram import F, Dispatcher, Router, Bot
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from handlers.class_state import HabitsState
from keyboards.back_kb import back_kb
from keyboards.requests_in_friends_kb import scroll_req_kb
from models.requests_to_habits import get_habit_by_name, get_all_habits_by_user_id, get_index_habit
from models.requests_to_users import get_tg_id_by_id
from keyboards.scroll_friends_kb import scroll_friends_kb
from keyboards.scrolling_habits_kb import scroll_habit_kb
from keyboards.about_achievement_kb import scroll_ach_kb
from models.requests_to_log_ach import get_ach_by_id
from decouple import config


bot = Bot(token = config('TOKEN'))
router = Router()


@router.callback_query(F.data.in_(['right', 'left']))
async def get_left_right(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    type_scroll = data.get('type')
    if type_scroll == 'habits':
        items = data.get("habits", [])
        kb_func = scroll_habit_kb
        msg = 'Нет привычек для отображения.'
    elif type_scroll == 'achievements':
        items = data.get("achievements", [])
        kb_func = scroll_ach_kb
        msg = 'Нет достижений для отображения.'

    elif type_scroll=='friends':
        items = data.get("friends", [])
        kb_func = scroll_friends_kb
        msg = 'Нет друзей для отображения.'

    elif type_scroll=='requests':
        items = data.get("requests", [])
        kb_func = scroll_req_kb()
        msg = 'Нет запросов для отображения.'

    else:
        raise ValueError('Type Not Found')

    index = data.get("index", 0)

    if not items:
        await callback_query.answer(msg)
        return

    if callback_query.data == "right":
        index = (index + 1) % len(items)

    elif callback_query.data == "left":
        index = (index - 1) % len(items)

    await state.update_data(index=index, key=items[index].id)

    current_item = items[index]
    if type_scroll == 'achievements':
        current_item = get_ach_by_id(current_item.id)

    if type_scroll == 'friends' or type_scroll == 'requests':
        tg_id = get_tg_id_by_id(current_item.fr2_id)
        user_chat = await bot.get_chat(tg_id)
        friend_name = user_chat.first_name
        await callback_query.message.edit_text(friend_name, reply_markup=kb_func())
        return

    await callback_query.message.edit_text(current_item.name, reply_markup=kb_func())


@router.callback_query(F.data == 'search_habit')
async def search_habit_by_name(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.answer('Введите привычку', reply_markup=ReplyKeyboardRemove())
    await state.set_state(HabitsState.waiting_for_input_state)


@router.message(HabitsState.waiting_for_input_state)
async def input_habit(message: Message, state: FSMContext):
    await state.clear()
    habit = get_habit_by_name(message.text, message.from_user.id)
    if not habit:
        await message.answer('Привычка не найдена, попробуйте ввести еще раз', reply_markup=back_kb())
        await state.set_state(HabitsState.waiting_for_input_state)
        return
    habits = get_all_habits_by_user_id(message.from_user.id)
    index = get_index_habit(habit, habits)
    await state.update_data(type="habits", habits=habits, index=index, key=habit.id)
    await message.answer(habit.name, reply_markup=scroll_habit_kb())