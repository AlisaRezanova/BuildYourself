from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def scroll_habit_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="<", callback_data="left"),
            InlineKeyboardButton(text="Ввести привычку", callback_data="search_habit"),
            InlineKeyboardButton(text=">", callback_data="right"),]
        ])
    return kb