from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_start_keyboard() -> InlineKeyboardMarkup:
    start_keyboard = InlineKeyboardBuilder()
    start_keyboard.button(text='Get random recipe', callback_data='shuffle')

    return start_keyboard.as_markup()


def get_shuffle_keyboard(url: str) -> InlineKeyboardMarkup:
    shuffle_keyboard = InlineKeyboardBuilder()
    shuffle_keyboard.button(text='Yes, I would love to cook this one!', url=url)
    shuffle_keyboard.button(text='No, i want to get another recipe', callback_data='reshuffle')

    shuffle_keyboard.adjust(1)
    return shuffle_keyboard.as_markup()
