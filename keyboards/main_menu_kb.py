from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Выбор привычки")
    kb.button(text="Создание новой привычки")
    kb.button(text="Мой профиль")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)