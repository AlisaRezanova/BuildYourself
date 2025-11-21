from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def coop_invite_kb(invite_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Принять", callback_data=f"accept_coop_{invite_id}"),
                InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_coop_{invite_id}")
            ]
        ]
    )
