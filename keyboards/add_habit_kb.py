from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def add_habit_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Добавить новую привычку")
    kb.button(text="Назад")
    kb.button(text="Главное меню")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)