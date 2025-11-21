from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def friends_choice_kb(friends, cancel_button=True):
    buttons = []
    for friend in friends:
        buttons.append([InlineKeyboardButton(text=f" {friend['name']}", callback_data=f"friend_{friend['id']}")])

    if cancel_button:
        buttons.append([InlineKeyboardButton(text=" Отмена", callback_data="cancel_coop")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)