from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def profile_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Статистика и прогресс")
    kb.button(text="Достижения и награды")
    kb.button(text="Мои друзья")
    kb.button(text="Запросы")
    kb.button(text="Главное меню")
    kb.adjust(5)
    return kb.as_markup(resize_keyboard=True)