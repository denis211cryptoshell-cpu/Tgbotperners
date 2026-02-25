from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.main_menu import (
    get_age_income_menu, get_credit_purpose_menu, get_limit_menu,
    get_experience_menu, get_back_and_main_keyboard, get_share_keyboard,
    get_credit_problem_menu
)
from states.user_states import CreditCardStates
from config import LINKS, PARTNER_LINKS
import database

router = Router()


@router.callback_query(F.data.startswith("credit_problem_"))
async def credit_problem(callback: CallbackQuery, state: FSMContext):
    """Выбор проблемы с кредиткой"""
    user_id = callback.from_user.id
    
    # Начинаем воронку кредитной карты
    database.start_funnel(user_id, "credit_card")
    
    problem_map = {
        "credit_problem_rate": "высокий процент",
        "credit_problem_limit": "маленький лимит",
        "credit_problem_fees": "скрытые комиссии",
        "credit_problem_none": "нет кредитки",
    }
    problem = problem_map.get(callback.data, "нет кредитки")
    database.update_funnel(user_id, "credit_card", f"problem:{problem}")
    
    await state.update_data(problem=problem)
    await state.set_state(CreditCardStates.age_income)
    await callback.message.edit_text(
        f"Понял, {problem} — это серьёзно! 💳\n\n"
        "Какой у тебя возраст?",
        reply_markup=get_age_income_menu()
    )


@router.callback_query(CreditCardStates.age_income)
async def credit_age_income(callback: CallbackQuery, state: FSMContext):
    """Выбор возраста"""
    age_map = {
        "credit_age_18_25": "18-25 лет",
        "credit_age_26_35": "26-35 лет",
        "credit_age_36_50": "36-50 лет",
        "credit_age_50plus": "50+ лет",
    }
    age = age_map.get(callback.data, "26-35 лет")
    await state.update_data(age=age)
    await state.set_state(CreditCardStates.purpose)
    await callback.message.edit_text(
        f"Возраст: {age} 👤\n\n"
        "На что тебе нужны деньги?",
        reply_markup=get_credit_purpose_menu()
    )


@router.callback_query(CreditCardStates.purpose)
async def credit_purpose(callback: CallbackQuery, state: FSMContext):
    """Выбор цели кредита"""
    purpose_map = {
        "credit_purpose_tech": "техника",
        "credit_purpose_travel": "путешествия",
        "credit_purpose_auto": "авто",
        "credit_purpose_home": "дом/ремонт",
    }
    purpose = purpose_map.get(callback.data, "техника")
    await state.update_data(purpose=purpose)
    await state.set_state(CreditCardStates.limit)
    await callback.message.edit_text(
        f"Цель: {purpose} 🎯\n\n"
        "Какой лимит тебе нужен?",
        reply_markup=get_limit_menu()
    )


@router.callback_query(CreditCardStates.limit)
async def credit_limit(callback: CallbackQuery, state: FSMContext):
    """Выбор лимита"""
    limit_map = {
        "credit_limit_100": "до 100к",
        "credit_limit_300": "100-300к",
        "credit_limit_500": "300-500к",
        "credit_limit_500plus": "500к+",
    }
    limit = limit_map.get(callback.data, "100-300к")
    await state.update_data(limit=limit)
    await state.set_state(CreditCardStates.experience)
    await callback.message.edit_text(
        f"Лимит: {limit} ₽ 💰\n\n"
        "Есть ли у тебя опыт с кредитами?",
        reply_markup=get_experience_menu()
    )


@router.callback_query(CreditCardStates.experience)
async def credit_experience(callback: CallbackQuery, state: FSMContext):
    """Финал ветки кредитной карты - рекомендация"""
    user_id = callback.from_user.id
    experience = "есть" if callback.data == "credit_exp_yes" else "нет"
    user_data = await state.get_data()

    await state.clear()

    # Завершаем воронку
    database.complete_funnel(user_id, "credit_card")

    # Используем партнёрскую ссылку
    partner_link = PARTNER_LINKS.get("credit_card", LINKS["credit_card"])
    
    # Логируем конверсию
    database.log_conversion(user_id, "credit_card", partner_link)

    # Рекомендация на основе данных
    limit_val = user_data.get('limit', '100-300к')
    purpose = user_data.get('purpose', 'техника')

    if "500к+" in limit_val:
        card_name = "Tinkoff Platinum"
        features = (
            "✅ Лимит до 1 млн ₽\n"
            "✅ 55 дней без процентов\n"
            "✅ До 1 года рассрочка у партнёров\n"
            "✅ Бесплатное обслуживание"
        )
    elif "300-500к" in limit_val:
        card_name = "Tinkoff Platinum"
        features = (
            "✅ Лимит до 500к ₽\n"
            "✅ 55 дней без процентов\n"
            "✅ Кэшбэк на все покупки\n"
            "✅ Бесплатное снятие наличных"
        )
    else:
        card_name = "Tinkoff Credit"
        features = (
            "✅ Лимит до 300к ₽\n"
            "✅ 55 дней без процентов\n"
            "✅ Минимальный платёж от 3%\n"
            "✅ Быстрое оформление"
        )

    await callback.message.edit_text(
        f"🎯 <b>Тебе подойдёт {card_name}!</b>\n\n"
        f"{features}\n\n"
        f"Цель: {purpose}\n"
        f"Опыт: {experience}\n\n"
        f"👉 <a href='{partner_link}'>Оформить карту</a>",
        reply_markup=get_share_keyboard(),
        disable_web_page_preview=True
    )


@router.callback_query(F.data == "back_credit_age")
async def back_credit_age(callback: CallbackQuery, state: FSMContext):
    """Назад из возраста к проблеме"""
    await state.set_state(None)
    await callback.message.edit_text(
        "💰 <b>Кредитная карта</b> — деньги в долг без процентов!\n\n"
        "Что не нравится в текущей кредитке (или почему хочешь новую)?",
        reply_markup=get_credit_problem_menu()
    )


@router.callback_query(F.data == "back_credit_purpose")
async def back_credit_purpose(callback: CallbackQuery, state: FSMContext):
    """Назад из цели к возрасту"""
    await state.set_state(CreditCardStates.age_income)
    await callback.message.edit_text(
        "Возвращаемся к вопросу о возрасте.\n\n"
        "Какой у тебя возраст?",
        reply_markup=get_age_income_menu()
    )


@router.callback_query(F.data == "back_credit_limit")
async def back_credit_limit(callback: CallbackQuery, state: FSMContext):
    """Назад из лимита к цели"""
    await state.set_state(CreditCardStates.purpose)
    await callback.message.edit_text(
        "Возвращаемся к выбору цели.\n\n"
        "На что тебе нужны деньги?",
        reply_markup=get_credit_purpose_menu()
    )


@router.callback_query(F.data == "back_credit_experience")
async def back_credit_experience(callback: CallbackQuery, state: FSMContext):
    """Назад из опыта к лимиту"""
    await state.set_state(CreditCardStates.limit)
    await callback.message.edit_text(
        "Возвращаемся к вопросу о лимите.\n\n"
        "Какой лимит тебе нужен?",
        reply_markup=get_limit_menu()
    )
