from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

def confirm_habit_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Изменить название")
    kb.button(text="Изменить длительность")
    kb.button(text="Изменить статус уведомлений")
    kb.button(text="Все правильно")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)