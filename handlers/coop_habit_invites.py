from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from models.requests_to_friendshabits import get_pending_coop_invites, accept_coop_habit, reject_coop_habit
from models.requests_to_habits import create_new_habit
from models.requests_to_friends import get_friendship_by_id, get_friend_name_by_tg_id
from models.requests_to_users import get_user_by_id
from keyboards.main_menu_kb import main_menu_kb
from keyboards.coop_invite_kb import coop_invite_kb


router = Router()


@router.message(F.text == "Приглашения на привычки")
async def show_coop_invites(message: Message, state: FSMContext):
    await state.clear()

    invites = get_pending_coop_invites(message.from_user.id)

    if not invites:
        await message.answer('У вас нет новых приглашений на совместные привычки', reply_markup=main_menu_kb())
        return

    for invite in invites:
        habit = invite.habits
        friendship = get_friendship_by_id(invite.friend_id)

        if friendship.fr1_id != message.from_user.id:
            sender_id = friendship.fr1_id
        else:
            sender_id = friendship.fr2_id

        sender = get_user_by_id(sender_id)
        if not sender:
            continue
        sender_name = await get_friend_name_by_tg_id(sender.tg_id)

        invite_message = (
            f"🎯 Вам пришло приглашение на совместную привычку!\n\n"
            f"От: {sender_name}\n"
            f"Привычка: {habit.name}\n"
            f"Длительность: {habit.day_len} дней\n\n"
            f"Принять приглашение?"
        )

        await message.answer(invite_message, reply_markup=coop_invite_kb(invite.id))


@router.callback_query(F.data.startswith('accept_coop_'))
async def accept_coop_invite(callback_query: CallbackQuery, state: FSMContext):
    invite_id = int(callback_query.data.split('_')[2])

    coop_habit = accept_coop_habit(invite_id, callback_query.from_user.id)

    if coop_habit:
        habit = coop_habit.habits
        await callback_query.message.edit_text(
            f"Вы приняли приглашение! Привычка '{habit.name}' создана."
        )

    else:
        await callback_query.answer('Ошибка при принятии приглашения')


@router.callback_query(F.data.startswith('reject_coop_'))
async def reject_coop_invite(callback_query: CallbackQuery, state: FSMContext):
    invite_id = int(callback_query.data.split('_')[2])

    reject_coop_habit(invite_id)
    await callback_query.message.edit_text("Вы отклонили приглашение на совместную привычку")