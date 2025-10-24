from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Женщина")
    kb.button(text="Мужчина")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)