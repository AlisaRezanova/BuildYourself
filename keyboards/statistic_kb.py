from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def statistic_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Выбрать привычку")
    kb.button(text="Главное меню")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_stat_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Прогресс за неделю", callback_data="Прогресс за неделю"),
            InlineKeyboardButton(text="Прогресс за месяц", callback_data="Прогресс за месяц"),
            InlineKeyboardButton(text="Прогресс за полгода", callback_data="Прогресс за полгода"),
            InlineKeyboardButton(text="Прогресс за год", callback_data="Прогресс за год"),]
        ])
    return kb


def search_habit_kb() -> ReplyKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ввести привычку", callback_data="Ввести привычку")]
    ])
    return kb