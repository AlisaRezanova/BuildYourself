from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def admin_kb() -> ReplyKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пользователи", callback_data="users")],
        [InlineKeyboardButton(text="Награды", callback_data="achievements")],
        [InlineKeyboardButton(text="Статистика по боту", callback_data="statistics_bots")]
    ])
    return kb


def admin_user_kb() -> ReplyKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Информация", callback_data="Информация")],
        [InlineKeyboardButton(text="Удалить пользователя", callback_data="delete_user")]
    ])
    return kb


def admin_back_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Главное меню")
    kb.button(text="/admin")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def scroll_users_kb() -> ReplyKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="<", callback_data="left"),
        InlineKeyboardButton(text="Информация", callback_data="Информация"),
        InlineKeyboardButton(text="Удалить пользователя", callback_data="delete_user"),
        InlineKeyboardButton(text=">", callback_data="right"), ]
    ])
    return kb


def get_more_information_about_user() -> ReplyKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Краткая информация", callback_data="close_info"),
        InlineKeyboardButton(text="Удалить пользователя", callback_data="delete_user"), ]
    ])
    return kb
