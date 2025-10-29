from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def scroll_req_hab_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="<", callback_data="left"),
            InlineKeyboardButton(text="Подтвердить", callback_data="accept_habit"),
            InlineKeyboardButton(text="Отклонить", callback_data="reject_habit"),
            InlineKeyboardButton(text=">", callback_data="right"),]
        ])
    return kb


def req_hab_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Подтвердить", callback_data="accept_habit"),
            InlineKeyboardButton(text="Отклонить", callback_data="reject_habit"),]
        ])
    return kb