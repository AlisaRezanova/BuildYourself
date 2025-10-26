from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def scroll_friends_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="<", callback_data="left"),
            InlineKeyboardButton(text="Добавить друга", callback_data="add_friend"),
            InlineKeyboardButton(text=">", callback_data="right"),]
        ])
    return kb


def add_friend_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить друга", callback_data="add_friend"),]
    ])
    return kb