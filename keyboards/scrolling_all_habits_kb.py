from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def scroll_all_habits_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='⬅️', callback_data='habit_left')
    kb.button(text='➡️', callback_data='habit_right')
    kb.button(text=' Отметиться за сегодня', callback_data='mark_today')
    kb.button(text='Отметиться за определенное число', callback_data='mark_date')
    kb.adjust(2, 2)
    return kb.as_markup()