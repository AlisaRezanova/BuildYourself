from aiogram import F, Dispatcher, Router
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, BufferedInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from keyboards.about_achievement_kb import about_achievement_kb, scroll_ach_kb
from keyboards.scrolling_habits_kb import scroll_habit_kb
from models.requests_to_log_ach import get_ach_by_user_id, get_ach_by_id
from keyboards.back_kb import back_kb


router = Router()


@router.message(F.text=='Достижения и награды')
async def get_my_achievements(message: Message, state: FSMContext):
    await state.clear()
    achievements = get_ach_by_user_id(message.from_user.id)

    temp_msg = await message.answer('...', reply_markup=back_kb())
    await temp_msg.delete()

    if not achievements:
        await message.answer('Достижений пока нет')
        return
    if len(achievements) == 1:
        await message.answer(achievements[0].name, reply_markup=about_achievement_kb())
    else:
        await state.update_data(type="achievements", achievements=achievements, index=0, key=achievements[0].id)
        current_ach = achievements[0]
        current_ach = get_ach_by_id(current_ach.id)
        await message.answer(current_ach.name, reply_markup=scroll_ach_kb())