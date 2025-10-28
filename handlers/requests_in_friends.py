from aiogram import F, Dispatcher, Router, Bot
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.requests_in_friends_kb import req_ac_rej, scroll_req_kb
from models.requests_to_friends import get_all_requests, update_fr_status
from models.requests_to_users import get_tg_id_by_id
from keyboards.back_kb import back_kb
from decouple import config


bot = Bot(token = config('TOKEN'))
router = Router()


@router.message(F.text=='Запросы в друзья')
async def get_friend_list_request(message: Message, state: FSMContext):
    await state.clear()

    requests = get_all_requests(message.from_user.id)

    temp_msg = await message.answer('...', reply_markup=back_kb())

    await temp_msg.delete()
    if not requests:
        await message.answer('Запросов пока нет')
        return
    if len(requests) == 1:
        current_req = requests[0]
        tg_id = get_tg_id_by_id(current_req.fr2_id)
        user_chat = await bot.get_chat(tg_id)
        friend_name = user_chat.first_name
        await state.update_data(key=requests[0].id)
        await message.answer(friend_name, reply_markup=req_ac_rej())
    else:
        await state.update_data(type="requests", friends=requests, index=0, key=requests[0].id)
        current_req = requests[0]
        tg_id = get_tg_id_by_id(current_req.fr2_id)
        user_chat = await bot.get_chat(tg_id)
        friend_name = user_chat.first_name
        await message.answer(friend_name, reply_markup=scroll_req_kb())


@router.callback_query(F.data.in_(['accept', 'reject']))
async def update_status(callback_query: CallbackQuery, state: FSMContext):
    req = await state.get_data()
    fr_id = req.get('key')
    update_fr_status(callback_query.data, fr_id)
