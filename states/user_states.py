from aiogram.fsm.state import State, StatesGroup


class BlackStates(StatesGroup):
    """Состояния для ветки Tinkoff Black"""
    problem = State()  # Что бесит больше?
    categories = State()  # Главные категории трат
    expenses = State()  # Траты в месяц
    savings = State()  # Есть сбережения?


class CreditCardStates(StatesGroup):
    """Состояния для ветки кредитной карты"""
    problem = State()  # Что не нравится в текущей кредитке?
    age_income = State()  # Возраст и доход
    purpose = State()  # На что нужны деньги?
    limit = State()  # Нужный лимит?
    experience = State()  # Опыт с кредитами?


class InvestmentStates(StatesGroup):
    """Состояния для ветки инвестиций"""
    problem = State()  # Что мешает начать?
    experience = State()  # Опыт инвестиций?
    amount = State()  # Сумма для старта?
    risk = State()  # Уровень риска?
    goal = State()  # Цель?


class OtherStates(StatesGroup):
    """Состояния для ветки страховка/связь"""
    choice = State()  # Выбор: страховка или связь
    details = State()  # Детали запроса
