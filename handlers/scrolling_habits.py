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
from handlers.earn_achievement import EarnAchievement
from models.requests_to_friendshabits import get_coop_progress
from keyboards.scrolling_all_habits_kb import scroll_all_habits_kb


router = Router()

@router.message(F.text == "Выбор привычки")
async def select_habit_handler(message: Message, state: FSMContext):
    await state.clear()
    habits = get_all_habits_by_user_id(message.from_user.id)

    if not habits:
        await message.answer('Привычек пока нет', reply_markup=main_menu_kb())
        return

    if len(habits) == 1:
        is_coop = habits[0].is_coop == 'yes'
        await message.answer(habits[0].name, reply_markup=scroll_all_habits_kb(is_coop=is_coop))
        await state.update_data(type = "habit_selection", habits = habits, index = 0, key = habits[0].id)
    else:
        is_coop = habits[0].is_coop == 'yes'
        await state.update_data(type = "habit_selection", habits = habits, index = 0, key = habits[0].id)
        current_habit = habits[0]
        await message.answer(current_habit.name, reply_markup = scroll_all_habits_kb(is_coop=is_coop))

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

    is_coop = current_habit.is_coop == 'yes'

    await callback_query.message.edit_text(current_habit.name, reply_markup=scroll_all_habits_kb(is_coop=is_coop))


@router.callback_query(F.data == "coop_progress")
async def show_coop_progress(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    habit_id = data.get('key')

    progress_info = get_coop_progress(habit_id, callback_query.from_user.id)

    if not progress_info:
        await callback_query.answer('Информация о совместном прогрессе недоступна')
        return

    progress_message = (
        f"Совместный прогресс: {progress_info['habit_name']}\n\n"
        f"Вы: {progress_info['user_progress_bar']} {progress_info['user_days']}/{progress_info['duration']} дней\n"
        f"{progress_info['friend_name']}: {progress_info['friend_progress_bar']} {progress_info['friend_days']}/{progress_info['duration']} дней\n\n"
        f"Общий прогресс: {progress_info['total_days']}/{progress_info['total_duration']} дней\n"
        f"До конца челленджа: {progress_info['days_remaining']} дней "
    )

    progress_message_id = data.get('progress_message_id')
    if progress_message_id:
        try:
            await callback_query.bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=progress_message_id,
                text=progress_message
            )
            await callback_query.answer()
            return
        except:
            pass
    sent_message = await callback_query.message.answer(progress_message)
    await state.update_data(progress_message_id=sent_message.message_id)
    await callback_query.answer()


@router.callback_query(F.data == "mark_today")
async def mark_today_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    habit_id = data.get('key')
    habits = data.get('habits', [])
    index = data.get('index', 0)

    if not habits or index >= len(habits):
        await callback_query.answer('Ошибка: привычка не найдена')
        return

    current_habit = habits[index]

    mark_habit_today(habit_id)

    awarded_achievements = EarnAchievement.check_mark_achievements(callback_query.from_user.id, habit_id)
    for achievement_id in awarded_achievements:
        achievement = EarnAchievement.get_achievement_by_id(achievement_id)
        achievement_image = EarnAchievement.get_achievement_image(achievement)

        if achievement_image:
            await callback_query.message.answer_photo(
                achievement_image,
                caption=f'🎉 Вы получили награду "{achievement.name}"!\n📝 {achievement.description}'
            )
        else:
            await callback_query.message.answer(f'🎉 Вы получили награду "{achievement.name}"!')
            await callback_query.message.answer(f'📝 {achievement.description}')

    await callback_query.answer(f'Привычка "{current_habit.name}" отмечена за сегодня!')



@router.callback_query(F.data == "mark_date")
async def mark_date_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    habit_id = data.get('key')
    habits = data.get('habits', [])
    index = data.get('index', 0)

    if not habits or index >= len(habits):
        await callback_query.answer('Ошибка: привычка не найдена')
        return

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

        awarded_achievements = EarnAchievement.check_mark_achievements(message.from_user.id, habit_id)

        for achievement_id in awarded_achievements:
            achievement = EarnAchievement.get_achievement_by_id(achievement_id)
            achievement_image = EarnAchievement.get_achievement_image(achievement)

            if achievement_image:
                await message.answer_photo(
                    achievement_image,
                    caption=f'🎉 Вы получили награду "{achievement.name}"!\n📝 {achievement.description}'
                )
            else:
                await message.answer(f'🎉 Вы получили награду "{achievement.name}"!')
                await message.answer(f'📝 {achievement.description}')

        await message.answer(
            f' Привычка "{habit_name}" отмечена за {input_date.strftime("%d.%m.%Y")}!',
            reply_markup=main_menu_kb()
        )
        await state.clear()

    except ValueError:
        await message.answer('Неверный формат даты. Введите дату в формате ДД.ММ.ГГГГ (например: 25.12.2024):')
