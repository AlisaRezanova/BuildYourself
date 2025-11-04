from aiogram import F, Bot, Dispatcher, Router
from aiogram.filters import Command
from decouple import config
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from keyboards.about_achievement_kb import about_achievement_kb, scroll_ach_kb
from keyboards.admin_kb import admin_kb, admin_back_kb, admin_user_kb, scroll_users_kb, get_more_information_about_user
from models.requests_to_ach import get_all_ach
from models.requests_to_users import get_all_users_to_admin, get_tg_id_by_id, get_more_information_about_user_by_id, \
    delete_user_by_id, get_count_new_users_by_week, get_count_new_users_by_month, get_count_new_users_by_year

bot = Bot(token = config('TOKEN'))
dp = Dispatcher(storage=MemoryStorage())

router = Router()

ADMIN = [int(x) for x in config('ADMIN').split(',')]

@router.message(Command('admin'))
async def get_admin(message: Message):
    print(message.from_user.id)
    if message.from_user.id in ADMIN:
        await message.answer('Панель для админа', reply_markup=admin_kb())


@router.callback_query(F.data=='users')
async def get_all_users(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    users = get_all_users_to_admin()
    temp_msg = await callback_query.message.answer('...', reply_markup=admin_back_kb())

    await temp_msg.delete()

    if not users:
        await callback_query.message.answer('Пользователей пока нет')
        return

    if len(users) == 1:
        current_user = users[0]
        tg_id = current_user.tg_id
        user_chat = await bot.get_chat(tg_id)
        user_name = user_chat.first_name
        await state.update_data(key=users[0].id)
        username = user_chat.username
        description = f'Имя пользователя: {user_name} \nТГ-id пользователя: {tg_id}\nUsername: {username}'
        msg = await callback_query.message.answer(description, reply_markup=admin_user_kb())
        await state.update_data(msg_id=msg.message_id)
    else:
        await state.update_data(type="users", users=users, index=0, key=users[0].id)
        current_user = users[0]
        tg_id = current_user.tg_id
        user_chat = await bot.get_chat(tg_id)
        user_name = user_chat.first_name
        username = user_chat.username
        description = f'Имя пользователя: {user_name} \nТГ-id пользователя: {tg_id}\nUsername: {username}'
        msg = await callback_query.message.answer(description, reply_markup=scroll_users_kb())
        await state.update_data(msg_id=msg.message_id)


@router.callback_query(F.data=='Информация')
async def get_all_info_user(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cur_user_id = data.get('key')
    msg_id = data.get('msg_id')
    info = get_more_information_about_user_by_id(cur_user_id)
    await callback_query.bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=msg_id, text=f'Количество привычек: {info["count_hab"]}\n Количество наград: {info["count_ach"]}' , reply_markup=get_more_information_about_user())


@router.callback_query(F.data == 'close_info')
async def close_description(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    users = data.get('users')
    index = data.get('index')
    current_user = users[index]
    tg_id = current_user.tg_id
    user_chat = await bot.get_chat(tg_id)
    user_name = user_chat.first_name
    await callback_query.message.delete()
    msg = await callback_query.message.answer(text=user_name, reply_markup=scroll_users_kb())
    await state.update_data(msg_id=msg.message_id)


@router.callback_query(F.data == 'delete_user')
async def close_description(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('key')
    index = data.get('index')
    delete_user_by_id(user_id)
    await callback_query.answer('Пользователь удален')
    users = get_all_users_to_admin()
    current_user = users[index]
    tg_id = current_user.tg_id
    user_chat = await bot.get_chat(tg_id)
    user_name = user_chat.first_name
    await callback_query.message.delete()
    msg = await callback_query.message.answer(text=user_name, reply_markup=scroll_users_kb())
    await state.update_data(msg_id=msg.message_id, users=users)


@router.callback_query(F.data == 'achievements')
async def get_all_achievements(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    achievements = get_all_ach()

    temp_msg = await callback_query.message.answer('...', reply_markup=admin_back_kb())
    await temp_msg.delete()

    if not achievements:
        await callback_query.message.answer('Достижений пока нет')
        return
    if len(achievements) == 1:
        current_ach = achievements[0]
        await callback_query.message.answer(current_ach.name, reply_markup=about_achievement_kb())
    else:
        await state.update_data(type="achievements", achievements=achievements, index=0, key=achievements[0].id)
        current_ach = achievements[0]
        msg = await callback_query.message.answer(current_ach.name, reply_markup=scroll_ach_kb())
        await state.update_data(msg_id = msg.message_id)


@router.callback_query(F.data == 'statistics_bots')
async def get_all_achievements(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    new_week_users = get_count_new_users_by_week()
    new_month_users = get_count_new_users_by_month()
    new_year_users = get_count_new_users_by_year()
    users_count = len(get_all_users_to_admin())
    description = f'Общее количество пользователей: {users_count}\nКоличество новых пользователь за неделю: {new_week_users}\nКоличество новых пользователей за месяц: {new_month_users}\nКоличество новых пользователей за год: {new_year_users}'
    await callback_query.message.answer(description, reply_markup=admin_back_kb())
