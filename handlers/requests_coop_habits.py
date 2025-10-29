from aiogram import F, Dispatcher, Router, Bot
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, BufferedInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from keyboards.back_kb import back_kb
from keyboards.requests_coop_habits_kb import req_hab_kb, scroll_req_hab_kb
from models.requests_to_friendshabits import get_all_requests_in_habits, update_status_coop_habit
from models.requests_to_habits import get_name_habit_by_id


router = Router()


@router.message(F.text == 'Запросы на ведение привычки')
async def get_all_req_habits(message: Message, state: FSMContext):
    await state.clear()
    coop_habits = get_all_requests_in_habits(message.from_user.id)
    temp_msg = await message.answer('...', reply_markup=back_kb())
    await temp_msg.delete()
    if not coop_habits:
        await message.answer('Запросов на привычки еще нет')
        return
    await state.update_data(type="coop_habits", friends=coop_habits, index=0, key=coop_habits[0].id)
    current_coop_habit_name = get_name_habit_by_id(coop_habits[0].id)
    if len(coop_habits) == 1:
        await message.answer(current_coop_habit_name, reply_markup=req_hab_kb())
    else:
        await message.answer(current_coop_habit_name, reply_markup=scroll_req_hab_kb())


@router.callback_query(F.data.in_(['accept_habit', 'reject_habit']))
async def get_update_status_coop_habit(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    key = data.get('key')
    update_status_coop_habit(key, callback_query.data)
