from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def scroll_req_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="<", callback_data="left"),
            InlineKeyboardButton(text="Принять", callback_data="accept"),
            InlineKeyboardButton(text="Отклонить", callback_data="reject"),
            InlineKeyboardButton(text=">", callback_data="right"),]
        ])
    return kb

def req_ac_rej():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Принять", callback_data="accept"),
            InlineKeyboardButton(text="Отклонить", callback_data="reject"),]
        ])
    return kb