from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def scroll_habit_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="<", callback_data="left"),
            InlineKeyboardButton(text="Прогресс за неделю", callback_data="Прогресс за неделю"),
            InlineKeyboardButton(text="Прогресс за месяц", callback_data="Прогресс за месяц"),
            InlineKeyboardButton(text="Прогресс за полгода", callback_data="Прогресс за полгода"),
            InlineKeyboardButton(text="Прогресс за год", callback_data="Прогресс за год"),
            InlineKeyboardButton(text="Ввести привычку", callback_data="search_habit"),
            InlineKeyboardButton(text=">", callback_data="right"),]
        ])
    return kb

