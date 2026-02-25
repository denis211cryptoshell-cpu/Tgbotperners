from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_back_keyboard() -> InlineKeyboardMarkup:
    """Кнопка Назад"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="back"
        )],
    ])
    return keyboard


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Кнопка Главное меню"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🏠 Главное меню",
            callback_data="main_menu"
        )],
    ])
    return keyboard


def get_back_and_main_keyboard() -> InlineKeyboardMarkup:
    """Кнопки Назад и Главное меню"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back"),
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu"),
        ],
    ])
    return keyboard


def get_share_keyboard() -> InlineKeyboardMarkup:
    """Кнопка Поделиться ботом"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📢 Поделиться ботом с другом",
            switch_inline_query="Посмотри этого бота! Поможет подобрать продукт Т-Банка под твои нужды 🚀"
        )],
    ])
    return keyboard
