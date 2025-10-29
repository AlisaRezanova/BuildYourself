from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def all_requests_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Запросы в друзья")
    kb.button(text="Запросы на ведение привычки")
    kb.button(text="Главное меню")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)