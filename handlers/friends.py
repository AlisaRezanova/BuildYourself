from aiogram import F, Dispatcher, Router, Bot
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, BufferedInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from models.requests_to_friends import get_all_friends_by_user_id, get_tg_id_by_id
from keyboards.back_kb import back_kb
from keyboards.scroll_friends_kb import scroll_friends_kb, add_friend_kb
from decouple import config


bot = Bot(token = config('TOKEN'))
router = Router()


@router.message(F.text=='Мои друзья')
async def get_my_friends(message: Message, state: FSMContext):
    await state.clear()

    friends = get_all_friends_by_user_id(message.from_user.id)

    temp_msg = await message.answer('...', reply_markup=back_kb())

    await temp_msg.delete()

    if not friends:
        await message.answer('Друзей пока нет')
        return
    if len(friends) == 1:
        current_fr = friends[0]
        tg_id = get_tg_id_by_id(current_fr.fr2_id)
        user_chat = await bot.get_chat(tg_id)
        friend_name = user_chat.first_name
        await message.answer(friend_name, reply_markup=add_friend_kb())
    else:
        await state.update_data(type="friends", friends=friends, index=0, key=friends[0].id)
        current_fr = friends[0]
        tg_id = get_tg_id_by_id(current_fr.fr2_id)
        user_chat = await bot.get_chat(tg_id)
        friend_name = user_chat.first_name
        await message.answer(friend_name, reply_markup=scroll_friends_kb())