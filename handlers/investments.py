from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.main_menu import (
    get_invest_experience_menu, get_amount_menu, get_risk_menu,
    get_goal_menu, get_back_and_main_keyboard, get_share_keyboard,
    get_invest_problem_menu
)
from states.user_states import InvestmentStates
from config import LINKS, PARTNER_LINKS
import database

router = Router()


@router.callback_query(F.data.startswith("invest_problem_"))
async def invest_problem(callback: CallbackQuery, state: FSMContext):
    """Выбор проблемы с инвестициями"""
    user_id = callback.from_user.id
    
    # Начинаем воронку инвестиций
    database.start_funnel(user_id, "investment")
    
    problem_map = {
        "invest_problem_start": "не знаю с чего начать",
        "invest_problem_money": "мало денег",
        "invest_problem_fear": "боюсь потерять",
        "invest_problem_time": "нет времени",
    }
    problem = problem_map.get(callback.data, "не знаю с чего начать")
    database.update_funnel(user_id, "investment", f"problem:{problem}")
    
    await state.update_data(problem=problem)
    await state.set_state(InvestmentStates.experience)
    await callback.message.edit_text(
        f"Понял, {problem} — это распространённая ситуация! 📊\n\n"
        "Какой у тебя опыт в инвестициях?",
        reply_markup=get_invest_experience_menu()
    )


@router.callback_query(InvestmentStates.experience)
async def invest_experience(callback: CallbackQuery, state: FSMContext):
    """Выбор опыта инвестиций"""
    experience_map = {
        "invest_exp_newbie": "новичок",
        "invest_exp_some": "есть небольшой опыт",
        "invest_exp_pro": "опытный инвестор",
    }
    experience = experience_map.get(callback.data, "новичок")
    await state.update_data(experience=experience)
    await state.set_state(InvestmentStates.amount)
    await callback.message.edit_text(
        f"Опыт: {experience} 📚\n\n"
        "С какой суммой готов начать?",
        reply_markup=get_amount_menu()
    )


@router.callback_query(InvestmentStates.amount)
async def invest_amount(callback: CallbackQuery, state: FSMContext):
    """Выбор суммы для старта"""
    amount_map = {
        "invest_amount_10": "до 10к",
        "invest_amount_50": "10-50к",
        "invest_amount_100": "50-100к",
        "invest_amount_100plus": "100к+",
    }
    amount = amount_map.get(callback.data, "10-50к")
    await state.update_data(amount=amount)
    await state.set_state(InvestmentStates.risk)
    await callback.message.edit_text(
        f"Сумма: {amount} ₽ 💰\n\n"
        "Какой уровень риска тебе комфортен?",
        reply_markup=get_risk_menu()
    )


@router.callback_query(InvestmentStates.risk)
async def invest_risk(callback: CallbackQuery, state: FSMContext):
    """Выбор уровня риска"""
    risk_map = {
        "invest_risk_low": "минимальный",
        "invest_risk_medium": "средний",
        "invest_risk_high": "высокий",
    }
    risk = risk_map.get(callback.data, "средний")
    await state.update_data(risk=risk)
    await state.set_state(InvestmentStates.goal)
    await callback.message.edit_text(
        f"Риск: {risk} ⚖️\n\n"
        "Какая у тебя цель инвестиций?",
        reply_markup=get_goal_menu()
    )


@router.callback_query(InvestmentStates.goal)
async def invest_goal(callback: CallbackQuery, state: FSMContext):
    """Финал ветки инвестиций - рекомендация"""
    user_id = callback.from_user.id
    goal_map = {
        "invest_goal_income": "пассивный доход",
        "invest_goal_capital": "накопить капитал",
        "invest_goal_purchase": "конкретная покупка",
    }
    goal = goal_map.get(callback.data, "пассивный доход")
    user_data = await state.get_data()

    await state.clear()

    # Завершаем воронку
    database.complete_funnel(user_id, "investment")

    # Используем партнёрскую ссылку
    partner_link = PARTNER_LINKS.get("investments", LINKS["investments"])
    
    # Логируем конверсию
    database.log_conversion(user_id, "investment", partner_link)

    # Рекомендация на основе данных
    experience = user_data.get('experience', 'новичок')
    amount = user_data.get('amount', '10-50к')
    risk = user_data.get('risk', 'средний')

    if experience == "новичок":
        recommendation = (
            "🎯 <b>ИИС (Индивидуальный инвестиционный счёт)</b>\n\n"
            "✅ Подарок акциями до 100к ₽\n"
            "✅ Налоговый вычет 13%\n"
            "✅ Доход до 20% без комиссии\n"
            "✅ Автоследование за стратегиями\n"
            "✅ Минимальный вход от 1000 ₽"
        )
    elif risk == "минимальный":
        recommendation = (
            "🎯 <b>Облигации и фонды денежного рынка</b>\n\n"
            "✅ Стабильный доход 12-16%\n"
            "✅ Минимальный риск\n"
            "✅ Ликвидность — можно продать в любой момент\n"
            "✅ Купоны каждый месяц"
        )
    else:
        recommendation = (
            "🎯 <b>Смешанный портфель</b>\n\n"
            "✅ Акции российских компаний\n"
            "✅ Облигации для стабильности\n"
            "✅ ETF на индексы\n"
            "✅ Доходность 15-25% годовых"
        )

    await callback.message.edit_text(
        f"🎯 <b>Рекомендация для тебя!</b>\n\n"
        f"{recommendation}\n\n"
        f"Цель: {goal}\n"
        f"Сумма: {amount} ₽\n\n"
        f"👉 <a href='{partner_link}'>Открыть брокерский счёт</a>",
        reply_markup=get_share_keyboard(),
        disable_web_page_preview=True
    )


@router.callback_query(F.data == "back_invest_experience")
async def back_invest_experience(callback: CallbackQuery, state: FSMContext):
    """Назад из опыта к проблеме"""
    await state.set_state(None)
    await callback.message.edit_text(
        "📈 <b>Инвестиции</b> — приумножь свои сбережения!\n\n"
        "Что мешает начать инвестировать?",
        reply_markup=get_invest_problem_menu()
    )


@router.callback_query(F.data == "back_invest_amount")
async def back_invest_amount(callback: CallbackQuery, state: FSMContext):
    """Назад из суммы к опыту"""
    await state.set_state(InvestmentStates.experience)
    await callback.message.edit_text(
        "Возвращаемся к вопросу об опыте.\n\n"
        "Какой у тебя опыт в инвестициях?",
        reply_markup=get_invest_experience_menu()
    )


@router.callback_query(F.data == "back_invest_risk")
async def back_invest_risk(callback: CallbackQuery, state: FSMContext):
    """Назад из риска к сумме"""
    await state.set_state(InvestmentStates.amount)
    await callback.message.edit_text(
        "Возвращаемся к вопросу о сумме.\n\n"
        "С какой суммой готов начать?",
        reply_markup=get_amount_menu()
    )


@router.callback_query(F.data == "back_invest_goal")
async def back_invest_goal(callback: CallbackQuery, state: FSMContext):
    """Назад из цели к риску"""
    await state.set_state(InvestmentStates.risk)
    await callback.message.edit_text(
        "Возвращаемся к вопросу о риске.\n\n"
        "Какой уровень риска тебе комфортен?",
        reply_markup=get_risk_menu()
    )
