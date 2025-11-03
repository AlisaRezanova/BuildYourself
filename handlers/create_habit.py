from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from keyboards.main_menu_kb import main_menu_kb
from keyboards.duration_choice_kb import duration_choice_kb
from keyboards.notification_need_kb import notification_choice_kb
from models.requests_to_habits import create_new_habit, get_all_habits_by_user_id, update_habit_duration, update_habit_notification

router = Router()


class HabitStates:
    waiting_for_habit_name = "waiting_for_habit_name"
    waiting_for_duration_choice = "waiting_for_duration_choice"
    waiting_for_notification_choice = "waiting_for_notification_choice"

@router.message(F.text == 'Создание новой привычки')
async def create_new_habit_handler(message: Message, state: FSMContext):
    await state.clear()

    await state.set_state(HabitStates.waiting_for_habit_name)
    await message.answer('Введите название привычки:', reply_markup=ReplyKeyboardRemove())


@router.message(StateFilter(HabitStates.waiting_for_habit_name))
async def process_habit_name(message: Message, state: FSMContext):
    habit_name = message.text.strip()

    if not habit_name:
        await message.answer('Название привычки не может быть пустым')
        return

    if len(habit_name) > 100:
        await message.answer('Название привычки слишком длинное (максимум 100 символов)')
        return

    habit_id = create_new_habit(message.from_user.id, habit_name)
    await state.update_data(habit_id=habit_id, habit_name=habit_name)
    await state.set_state(HabitStates.waiting_for_duration_choice)
    await message.answer(f'Привычка "{habit_name}" успешно создана!')
    await message.answer('Выберите длительность привычки:', reply_markup=duration_choice_kb())

@router.message(StateFilter(HabitStates.waiting_for_duration_choice), F.text.in_(['1 неделя', '2 месяца', '6 месяцев', '1 год']))
async def process_duration_choice(message: Message, state: FSMContext):
    data = await state.get_data()
    habit_id = data.get('habit_id')
    habit_name = data.get('habit_name')

    duration_map = {
        '1 неделя': 7,
        '2 месяца': 60,
        '6 месяцев': 180,
        '1 год': 365
    }

    duration_days = duration_map[message.text]
    update_habit_duration(habit_id, duration_days)

    await state.update_data(duration_days=duration_days, duration_text=message.text)
    await state.set_state(HabitStates.waiting_for_notification_choice)
    await message.answer(f'Длительность привычки установлена: {message.text}')
    await message.answer('Нужны ли уведомления?', reply_markup=notification_choice_kb())

@router.message(StateFilter(HabitStates.waiting_for_notification_choice), F.text.in_(['Уведомления нужны', 'Уведомления не нужны']))
async def process_notification_choice(message: Message, state: FSMContext):
    data = await state.get_data()
    habit_id = data.get('habit_id')
    habit_name = data.get('habit_name')
    duration_text = data.get('duration_text')

    notification = True if message.text == 'Уведомления нужны' else False
    update_habit_notification(habit_id, notification)

    notification_text = 'включены' if notification else 'выключены'
    await message.answer(f'Уведомления {notification_text}')
    await message.answer(
        f'Привычка "{habit_name}" успешно создана!\nДлительность: {duration_text}\nУведомления: {notification_text}',
        reply_markup=main_menu_kb())
    await state.clear()