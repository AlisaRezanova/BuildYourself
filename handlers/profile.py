from aiogram import F, Dispatcher, Router
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, BufferedInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from keyboards.profile_kb import profile_kb
from keyboards.statistic_kb import statistic_kb, get_stat_kb
from models.requests_to_habits import get_all_habits_by_user_id
from keyboards.add_habit_kb import add_habit_kb
from keyboards.scrolling_habits_kb import scroll_habit_kb
from keyboards.back_kb import back_kb
from models.requests_to_log_habits import get_progress_by_week, get_progress_by_month, get_progress_by_half_year, get_progress_by_year


router = Router()


@router.message(F.text == 'Мой профиль')
async def get_profile(message: Message):
    await message.answer('Некоторая информация о профиле...', reply_markup=profile_kb())


@router.message(F.text == 'Статистика и прогресс')
async def get_statistic(message: Message):
    await message.answer('...', reply_markup=statistic_kb())


@router.message(F.text == 'Выбрать привычку')
async def get_all_habits(message: Message, state: FSMContext):
    await state.clear()
    habits = get_all_habits_by_user_id(message.from_user.id)
    temp_msg = await message.answer('...', reply_markup=back_kb())
    await temp_msg.delete()
    if not habits:
        await message.answer('Привычек пока нет', reply_markup=add_habit_kb())
        return
    if len(habits) == 1:
        await message.answer(habits[0].name, reply_markup=get_stat_kb())
    else:
        await state.update_data(type="habits", habits=habits, index=0, key=habits[0].id)
        current_habit = habits[0]
        await message.answer(current_habit.name, reply_markup=scroll_habit_kb())


@router.callback_query(F.data.startswith('Прогресс за'))
async def get_stat_by_range(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    habit_id = data.get('key')
    msg_id = data.get('msg_id')
    if callback_query.data == 'Прогресс за неделю':
        buf = get_progress_by_week(habit_id)
    elif callback_query.data == 'Прогресс за месяц':
        buf = get_progress_by_month( habit_id)
    elif callback_query.data == 'Прогресс за полгода':
        buf = get_progress_by_half_year(habit_id)
    elif callback_query.data == 'Прогресс за год':
        buf = get_progress_by_year(habit_id)
    else:
        raise ValueError('Нет графика(')
    if buf is None:
        await callback_query.message.answer('Нет данных по этой привычке.')  # Добавить назад ко всем привычкам
        return
    photo = BufferedInputFile(buf.getvalue(), filename='progress.png')

    if msg_id:
        await callback_query.bot.edit_message_media(chat_id=callback_query.message.chat.id, message_id=msg_id, media=InputMediaPhoto(media=photo))
    else:
        msg = await callback_query.message.answer_photo(photo)
        await state.update_data(msg_id=msg.message_id)



