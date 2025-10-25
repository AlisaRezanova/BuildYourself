from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def statistic_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Выбрать привычку")
    kb.button(text="Главное меню")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_stat_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Прогресс за неделю")
    kb.button(text="Прогресс за месяц")
    kb.button(text="Прогресс за полгода")
    kb.button(text="Прогресс за год")
    kb.button(text="Главное меню")
    kb.adjust(5)
    return kb.as_markup(resize_keyboard=True)


def search_habit_kb() -> ReplyKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ввести привычку", callback_data="Ввести привычку")]
    ])
    return kb