from aiogram import F, Dispatcher, Router
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from keyboards.scrolling_habits_kb import scroll_habit_kb
from keyboards.statistic_kb import statistic_kb


router = Router()


@router.callback_query(F.data.in_(['right', 'left']))
async def get_right(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    habits = data.get("habits", [])
    index = data.get("index", 0)
    if not habits:
        await callback_query.answer("Нет привычек для отображения.")
        return
    if callback_query.data == "right":
        index = (index + 1) % len(habits)
    elif callback_query.data == "left":
        index = (index - 1) % len(habits)

    await state.update_data(index=index, hab_id=habits[index].id)

    current_habit = habits[index]
    await callback_query.message.edit_text(current_habit.name, reply_markup=scroll_habit_kb())


@router.callback_query(F.data == 'search_habit')
async def search_habit_by_name(message: Message, state: FSMContext):
    ...