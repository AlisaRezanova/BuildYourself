from aiogram import F, Dispatcher, Router, Bot
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, BufferedInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from handlers.class_state import FriendsState
from keyboards.my_friends_kb import my_friends_kb
from models.requests_to_friends import get_all_friends_by_user_id, add_note_friends, \
    check_eq_invite_code, update_friends2, delete_friend_by_id
from models.requests_to_users import get_tg_id_by_id, get_user_id_by_tg_id
from keyboards.back_kb import back_kb
from keyboards.scroll_friends_kb import scroll_friends_kb, add_friend_kb
from decouple import config
import random, string


bot = Bot(token = config('TOKEN'))
router = Router()


@router.message(F.text=='Мои друзья')
async def get_my_friends(message: Message):
    await message.answer('Выберите действие', reply_markup=my_friends_kb())


@router.message(F.text=='Просмотр друзей')
async def get_friend_list(message: Message, state: FSMContext):
    await state.clear()

    friends = get_all_friends_by_user_id(message.from_user.id)

    temp_msg = await message.answer('...', reply_markup=back_kb())

    await temp_msg.delete()

    if not friends:
        await message.answer('Друзей пока нет')
        return

    if len(friends) == 1:
        current_fr = friends[0]
        current_user_id = get_user_id_by_tg_id(message.from_user.id)

        if current_fr.fr1_id == current_user_id:
            friend_id = current_fr.fr2_id
        else:
            friend_id = current_fr.fr1_id

        tg_id = get_tg_id_by_id(friend_id)
        user_chat = await bot.get_chat(tg_id)
        friend_name = user_chat.first_name
        await state.update_data(key=friends[0].id)
        await message.answer(friend_name, reply_markup=add_friend_kb())
    else:
        await state.update_data(type="friends", friends=friends, index=0, key=friends[0].id)
        current_fr = friends[0]
        current_user_id = get_user_id_by_tg_id(message.from_user.id)

        if current_fr.fr1_id == current_user_id:
            friend_id = current_fr.fr2_id
        else:
            friend_id = current_fr.fr1_id

        tg_id = get_tg_id_by_id(friend_id)

        user_chat = await bot.get_chat(tg_id)
        friend_name = user_chat.first_name
        await message.answer(friend_name, reply_markup=scroll_friends_kb())


def generate_invite_code():
    alf= ''.join(i for i in string.digits+string.ascii_letters)
    code = ''.join(random.choice(alf) for _ in range(8))
    return check_eq_invite_code(code)


@router.message(F.text=='Сгенерировать личный код для присоединения')
async def get_invite_code(message: Message):
    invite_code = generate_invite_code()
    add_note_friends(message.from_user.id, invite_code)
    await message.answer(invite_code, reply_markup=back_kb())


@router.message(F.text=='Добавить друга')
async def add_friend(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(FriendsState.waiting_for_invite_code)
    await message.answer('Введите код приглашения', reply_markup=back_kb())


@router.callback_query(F.data=='add_friend')
async def add_friend(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(FriendsState.waiting_for_invite_code)
    await callback_query.message.answer('Введите код приглашения', reply_markup=back_kb())


@router.message(FriendsState.waiting_for_invite_code)
async def input_invite_code(message: Message, state: FSMContext):
    await state.clear()
    update_friends2(message.from_user.id, message.text)
    await message.answer('Ждем одобрения вашей заявки', reply_markup=back_kb())


@router.callback_query(F.data=='delete_friend')
async def delete_friend(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    fr_id = data.get('key')
    delete_friend_by_id(fr_id)
    await callback_query.message.delete()
    fake_message = callback_query.message
    fake_message.text = 'Просмотр друзей'
    await get_friend_list(fake_message, state)





