from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def notification_choice_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Уведомления нужны')
    kb.button(text='Уведомления не нужны')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)