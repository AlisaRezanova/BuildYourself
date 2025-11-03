from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def duration_choice_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='1 неделя')
    kb.button(text='2 месяца')
    kb.button(text='6 месяцев')
    kb.button(text='1 год')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)