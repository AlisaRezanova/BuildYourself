from aiogram import F, Dispatcher, Router
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, BufferedInputFile, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext
from keyboards.about_achievement_kb import about_achievement_kb, scroll_ach_kb, close_description_kb
from keyboards.admin_kb import scroll_ach_in_admin_kb
from models.requests_to_ach import get_description_about_ach
from models.requests_to_log_ach import get_ach_by_user_id, get_ach_by_id, get_count_ach_by_id
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
        current_ach = achievements[0]
        current_ach = get_ach_by_id(current_ach.id)
        msg = await message.answer(current_ach.name, reply_markup=about_achievement_kb())
        await state.update_data(msg_id=msg.message_id, key=achievements[0].id)
    else:
        await state.update_data(type="achievements", achievements=achievements, index=0, key=achievements[0].id)
        current_ach = achievements[0]
        current_ach = get_ach_by_id(current_ach.id)
        msg = await message.answer(current_ach.name, reply_markup=scroll_ach_kb())
        await state.update_data(msg_id = msg.message_id)


@router.callback_query(F.data == 'more')
async def get_more_about_ach(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    ach_id = data.get('key')
    msg_id = data.get('msg_id')
    img, description = get_description_about_ach(ach_id)
    if data.get('is_admin'):
        description += f'\nКоличество людей, имеющих данное достижение: {get_count_ach_by_id(ach_id)}'
    if img is None:
        await callback_query.bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=msg_id, text=description,
                                                    reply_markup=close_description_kb())
    else:
        photo = FSInputFile(img, filename='ach.png')
        await callback_query.bot.edit_message_media(chat_id=callback_query.message.chat.id, message_id=msg_id,
                                                media=InputMediaPhoto(media=photo, caption=description), reply_markup=close_description_kb())


@router.callback_query(F.data == 'close')
async def close_description(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    ach_id = data.get('key')
    current_ach = get_ach_by_id(ach_id)
    await callback_query.message.delete()
    if data.get('is_admin'):
        kb = scroll_ach_in_admin_kb
    else:
        kb = scroll_ach_kb
    msg = await callback_query.message.answer(text=current_ach.name, reply_markup=kb())
    await state.update_data(msg_id=msg.message_id)