from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def scroll_all_habits_kb(is_coop=False):
    buttons = [
        [InlineKeyboardButton(text="⬅️", callback_data="habit_left"),
         InlineKeyboardButton(text="➡️", callback_data="habit_right")],
        [InlineKeyboardButton(text="Отметиться за сегодня", callback_data="mark_today")],
        [InlineKeyboardButton(text="Отметиться за определенное число", callback_data="mark_date")]
    ]

    if is_coop:
        buttons.append([InlineKeyboardButton(text="Прогресс с другом", callback_data="coop_progress")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)