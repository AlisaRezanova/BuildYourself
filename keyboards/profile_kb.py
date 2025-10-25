from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def profile_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Статистика и прогресс")
    kb.button(text="Достижения и награды")
    kb.button(text="Мои друзья")
    kb.button(text="Запросы в друзья")
    kb.button(text="Назад")
    kb.button(text="Главное меню")
    kb.adjust(6)
    return kb.as_markup(resize_keyboard=True)