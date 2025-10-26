from aiogram import F, Dispatcher, Router, Bot
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from models.requests_to_friends import get_tg_id_by_id
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
    if type_scroll == 'friends':
        tg_id = get_tg_id_by_id(current_item.fr2_id)
        user_chat = await bot.get_chat(tg_id)
        friend_name = user_chat.first_name
        await callback_query.message.edit_text(friend_name, reply_markup=kb_func())
        return
    await callback_query.message.edit_text(current_item.name, reply_markup=kb_func())


@router.callback_query(F.data == 'search_habit')
async def search_habit_by_name(message: Message, state: FSMContext):
    ...