from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def habit_type_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Обычная привычка'), KeyboardButton(text='Совместная привычка')]
        ],
        resize_keyboard=True
    )
    return kb