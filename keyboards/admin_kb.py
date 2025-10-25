from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def admin_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Пользователи")
    kb.button(text="Награды")
    kb.button(text="Статистика по боту")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)


def admin_user_kb() -> ReplyKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Статистика", callback_data="Статистика")],
        [InlineKeyboardButton(text="Удалить пользователя", callback_data="Удалить пользователя")]
    ])
    return kb
