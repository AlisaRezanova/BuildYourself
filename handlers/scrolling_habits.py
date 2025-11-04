from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from models.requests_to_habits import get_all_habits_by_user_id
from models.requests_to_log_habits import mark_habit_today, mark_habit_by_date
from keyboards.scrolling_all_habits_kb import scroll_all_habits_kb
from keyboards.main_menu_kb import main_menu_kb
from handlers.class_state import HabitMarkDate
from datetime import date, datetime


router = Router()

@router.message(F.text == "Выбор привычки")
async def select_habit_handler(message: Message, state: FSMContext):
    await state.clear()
    habits = get_all_habits_by_user_id(message.from_user.id)

    if not habits:
        await message.answer('Привычек пока нет', reply_markup=main_menu_kb())
        return

    if len(habits) == 1:
        await message.answer(habits[0].name, reply_markup=scroll_all_habits_kb())
    else:
        await state.update_data(type = "habit_selection", habits = habits, index = 0, key = habits[0].id)
        current_habit = habits[0]
        await message.answer(current_habit.name, reply_markup = scroll_all_habits_kb())

@router.callback_query(F.data.in_(['habit_left', 'habit_right']))
async def scroll_all_habits(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    type_scroll = data.get('type')

    if type_scroll != 'habit_selection':
        await callback_query.answer('Неверный тип прокрутки')
        return
    habits = data.get("habits", [])
    index = data.get("index", 0)

    if not habits:
        await callback_query.answer('У вас еще нет привычек')
        return

    if callback_query.data == "habit_right":
        index = (index + 1) % len(habits)
    elif callback_query.data == "habit_left":
        index = (index - 1) % len(habits)

    await state.update_data(index=index, key=habits[index].id)
    current_habit = habits[index]

    await callback_query.message.edit_text(current_habit.name, reply_markup=scroll_all_habits_kb())

@router.callback_query(F.data == "mark_today")
async def mark_today_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    habit_id = data.get('key')
    habits = data.get('habits')
    index = data.get('index', 0)
    current_habit = habits[index]

    mark_habit_today(habit_id)
    await callback_query.answer(f'Привычка "{current_habit.name}" отмечена за сегодня!')


@router.callback_query(F.data == "mark_date")
async def mark_date_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    habit_id = data.get('key')
    habits = data.get('habits')
    index = data.get('index', 0)
    current_habit = habits[index]

    await state.update_data(
        mark_habit_id=habit_id,
        mark_habit_name=current_habit.name
    )

    await state.set_state(HabitMarkDate.waiting_for_date)

    await callback_query.message.answer(
        f'Введите дату для привычки "{current_habit.name}" в формате ДД.ММ.ГГГГ'
    )
    await callback_query.answer()

@router.message(StateFilter(HabitMarkDate.waiting_for_date))
async def process_date_input(message: Message, state: FSMContext):
    try:
        input_date = datetime.strptime(message.text, '%d.%m.%Y').date()


        if input_date > date.today():
            await message.answer('Нельзя отмечать привычки за будущие даты. Введите корректную дату:')
            return

        data = await state.get_data()
        habit_id = data.get('mark_habit_id')
        habit_name = data.get('mark_habit_name')


        mark_habit_by_date(habit_id, input_date)

        await message.answer(
            f' Привычка "{habit_name}" отмечена за {input_date.strftime("%d.%m.%Y")}!',
            reply_markup=main_menu_kb()
        )
        await state.clear()

    except ValueError:
        await message.answer('Неверный формат даты. Введите дату в формате ДД.ММ.ГГГГ (например: 25.12.2024):')
