from aiogram import F, Dispatcher, Router
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.profile_kb import profile_kb
from keyboards.statistic_kb import statistic_kb, get_stat_kb
from models.requests_to_habits import get_all_habits_by_user_id
from keyboards.add_habit_kb import add_habit_kb
from keyboards.scrolling_habits_kb import scroll_habit_kb
from keyboards.back_kb import back_kb


router = Router()


@router.message(F.text == 'Мой профиль')
async def get_profile(message: Message):
    await message.answer('Некоторая информация о профиле...', reply_markup=profile_kb())


@router.message(F.text == 'Статистика и прогресс')
async def get_statistic(message: Message):
    await message.answer('...', reply_markup=statistic_kb())


@router.message(F.text == 'Выбрать привычку')
async def get_all_habits(message: Message, state: FSMContext):
    habits = get_all_habits_by_user_id(message.from_user.id)
    temp_msg = await message.answer('...', reply_markup=back_kb())
    await temp_msg.delete()
    if not habits:
        await message.answer('Привычек пока нет', reply_markup=add_habit_kb())
        return
    if len(habits) == 1:
        await message.answer(habits[0].name, reply_markup=get_stat_kb())
    else:
        await state.update_data(habits=habits, index=0)
        current_habit = habits[0]
        await message.answer(current_habit.name, reply_markup=scroll_habit_kb())


@router.message(F.text == '.............')
async def get_stat_by_range(message: Message):
    ...




