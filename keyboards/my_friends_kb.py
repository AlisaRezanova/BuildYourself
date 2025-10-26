from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def my_friends_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Просмотр друзей")
    kb.button(text="Сгенерировать личный код для присоединения")
    kb.button(text="Добавить друга")
    kb.button(text="Главное меню")
    kb.adjust(4)
    return kb.as_markup(resize_keyboard=True)