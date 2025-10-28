from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def scroll_ach_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="<", callback_data="left"),
            InlineKeyboardButton(text="Узнать больше", callback_data="more"),
            InlineKeyboardButton(text=">", callback_data="right"),]
        ])
    return kb


def about_achievement_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Узнать больше", callback_data="more"),]
        ])
    return kb


def close_description_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Закрыть описание", callback_data="close"), ]
    ])
    return kb