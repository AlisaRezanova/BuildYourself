from aiogram import F, Dispatcher, Router
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from keyboards.scrolling_habits_kb import scroll_habit_kb
from keyboards.statistic_kb import statistic_kb
from keyboards.about_achievement_kb import scroll_ach_kb
from models.requests_to_log_ach import get_ach_by_id


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
    await callback_query.message.edit_text(current_item.name, reply_markup=kb_func())


@router.callback_query(F.data == 'search_habit')
async def search_habit_by_name(message: Message, state: FSMContext):
    ...