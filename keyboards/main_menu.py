from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu() -> InlineKeyboardMarkup:
    """Главное меню бота"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="💳 Мало кэшбэка и высокие комиссии",
            callback_data="black_card"
        )],
        [InlineKeyboardButton(
            text="💰 Нужны деньги в долг без процентов",
            callback_data="credit_card"
        )],
        [InlineKeyboardButton(
            text="📈 Хочу приумножить сбережения",
            callback_data="investments"
        )],
        [InlineKeyboardButton(
            text="📱 Дорогая страховка/связь",
            callback_data="other_products"
        )],
        [InlineKeyboardButton(
            text="🧮 Калькулятор выгоды",
            callback_data="calculator_menu"
        )],
        [InlineKeyboardButton(
            text="🎁 Просто акции",
            callback_data="promo"
        )],
    ])
    return keyboard


def get_black_menu() -> InlineKeyboardMarkup:
    """Меню для ветки Black"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="😡 Комиссии",
            callback_data="black_problem_fees"
        )],
        [InlineKeyboardButton(
            text="📉 Низкий кэшбэк",
            callback_data="black_problem_cashback"
        )],
        [InlineKeyboardButton(
            text="💸 Нет % на остаток",
            callback_data="black_problem_percent"
        )],
    ])
    return keyboard


def get_categories_menu() -> InlineKeyboardMarkup:
    """Выбор категорий трат"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🛒 Супермаркеты",
            callback_data="black_cat_supermarkets"
        )],
        [InlineKeyboardButton(
            text="⛽ АЗС",
            callback_data="black_cat_gas"
        )],
        [InlineKeyboardButton(
            text="✈️ Путешествия",
            callback_data="black_cat_travel"
        )],
        [InlineKeyboardButton(
            text="🔄 Всё подряд",
            callback_data="black_cat_all"
        )],
        [InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="back_black_categories"
        )],
    ])
    return keyboard


def get_expenses_menu() -> InlineKeyboardMarkup:
    """Выбор суммы трат в месяц"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="До 20к ₽",
            callback_data="black_exp_up20"
        )],
        [InlineKeyboardButton(
            text="20–50к ₽",
            callback_data="black_exp_20_50"
        )],
        [InlineKeyboardButton(
            text="50–100к ₽",
            callback_data="black_exp_50_100"
        )],
        [InlineKeyboardButton(
            text="100к+ ₽",
            callback_data="black_exp_100plus"
        )],
        [InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="back_black_expenses"
        )],
    ])
    return keyboard


def get_savings_menu() -> InlineKeyboardMarkup:
    """Вопрос про сбережения"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="✅ Да",
            callback_data="black_savings_yes"
        )],
        [InlineKeyboardButton(
            text="❌ Нет",
            callback_data="black_savings_no"
        )],
        [InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="back_black_savings"
        )],
    ])
    return keyboard


def get_credit_problem_menu() -> InlineKeyboardMarkup:
    """Проблемы с текущей кредиткой"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📊 Высокий процент",
            callback_data="credit_problem_rate"
        )],
        [InlineKeyboardButton(
            text="💸 Маленький лимит",
            callback_data="credit_problem_limit"
        )],
        [InlineKeyboardButton(
            text="📄 Скрытые комиссии",
            callback_data="credit_problem_fees"
        )],
        [InlineKeyboardButton(
            text="🆕 Нет кредитки",
            callback_data="credit_problem_none"
        )],
    ])
    return keyboard


def get_age_income_menu() -> InlineKeyboardMarkup:
    """Возраст и доход"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="18–25 лет",
            callback_data="credit_age_18_25"
        )],
        [InlineKeyboardButton(
            text="26–35 лет",
            callback_data="credit_age_26_35"
        )],
        [InlineKeyboardButton(
            text="36–50 лет",
            callback_data="credit_age_36_50"
        )],
        [InlineKeyboardButton(
            text="50+ лет",
            callback_data="credit_age_50plus"
        )],
        [InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="back_credit_age"
        )],
    ])
    return keyboard


def get_credit_purpose_menu() -> InlineKeyboardMarkup:
    """На что нужны деньги"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📱 Техника",
            callback_data="credit_purpose_tech"
        )],
        [InlineKeyboardButton(
            text="🌴 Путешествия",
            callback_data="credit_purpose_travel"
        )],
        [InlineKeyboardButton(
            text="🚗 Авто",
            callback_data="credit_purpose_auto"
        )],
        [InlineKeyboardButton(
            text="🏠 Дом/ремонт",
            callback_data="credit_purpose_home"
        )],
        [InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="back_credit_purpose"
        )],
    ])
    return keyboard


def get_limit_menu() -> InlineKeyboardMarkup:
    """Нужный лимит"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="До 100к ₽",
            callback_data="credit_limit_100"
        )],
        [InlineKeyboardButton(
            text="100–300к ₽",
            callback_data="credit_limit_300"
        )],
        [InlineKeyboardButton(
            text="300–500к ₽",
            callback_data="credit_limit_500"
        )],
        [InlineKeyboardButton(
            text="500к+ ₽",
            callback_data="credit_limit_500plus"
        )],
        [InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="back_credit_limit"
        )],
    ])
    return keyboard


def get_experience_menu() -> InlineKeyboardMarkup:
    """Опыт с кредитами"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="✅ Есть опыт",
            callback_data="credit_exp_yes"
        )],
        [InlineKeyboardButton(
            text="❌ Нет опыта",
            callback_data="credit_exp_no"
        )],
        [InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="back_credit_experience"
        )],
    ])
    return keyboard


def get_invest_problem_menu() -> InlineKeyboardMarkup:
    """Что мешает начать инвестировать"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🤔 Не знаю с чего начать",
            callback_data="invest_problem_start"
        )],
        [InlineKeyboardButton(
            text="💰 Мало денег",
            callback_data="invest_problem_money"
        )],
        [InlineKeyboardButton(
            text="😰 Боюсь потерять",
            callback_data="invest_problem_fear"
        )],
        [InlineKeyboardButton(
            text="⏱ Нет времени",
            callback_data="invest_problem_time"
        )],
    ])
    return keyboard


def get_invest_experience_menu() -> InlineKeyboardMarkup:
    """Опыт инвестиций"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🆕 Новичок",
            callback_data="invest_exp_newbie"
        )],
        [InlineKeyboardButton(
            text="📚 Есть небольшой опыт",
            callback_data="invest_exp_some"
        )],
        [InlineKeyboardButton(
            text="🎯 Опытный инвестор",
            callback_data="invest_exp_pro"
        )],
        [InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="back_invest_experience"
        )],
    ])
    return keyboard


def get_amount_menu() -> InlineKeyboardMarkup:
    """Сумма для старта"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="До 10к ₽",
            callback_data="invest_amount_10"
        )],
        [InlineKeyboardButton(
            text="10–50к ₽",
            callback_data="invest_amount_50"
        )],
        [InlineKeyboardButton(
            text="50–100к ₽",
            callback_data="invest_amount_100"
        )],
        [InlineKeyboardButton(
            text="100к+ ₽",
            callback_data="invest_amount_100plus"
        )],
        [InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="back_invest_amount"
        )],
    ])
    return keyboard


def get_risk_menu() -> InlineKeyboardMarkup:
    """Уровень риска"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🛡 Минимальный",
            callback_data="invest_risk_low"
        )],
        [InlineKeyboardButton(
            text="⚖️ Средний",
            callback_data="invest_risk_medium"
        )],
        [InlineKeyboardButton(
            text="🚀 Высокий",
            callback_data="invest_risk_high"
        )],
        [InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="back_invest_risk"
        )],
    ])
    return keyboard


def get_goal_menu() -> InlineKeyboardMarkup:
    """Цель инвестиций"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🏖 Пассивный доход",
            callback_data="invest_goal_income"
        )],
        [InlineKeyboardButton(
            text="📈 Накопить капитал",
            callback_data="invest_goal_capital"
        )],
        [InlineKeyboardButton(
            text="🎯 Конкретная покупка",
            callback_data="invest_goal_purchase"
        )],
        [InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="back_invest_goal"
        )],
    ])
    return keyboard


def get_other_menu() -> InlineKeyboardMarkup:
    """Выбор: страховка или связь"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📱 T-Mobile (связь)",
            callback_data="other_tmobile"
        )],
        [InlineKeyboardButton(
            text="🛡 Страхование",
            callback_data="other_insurance"
        )],
    ])
    return keyboard


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
