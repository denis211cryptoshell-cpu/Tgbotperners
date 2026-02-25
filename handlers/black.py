from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.main_menu import (
    get_categories_menu, get_expenses_menu, get_savings_menu,
    get_back_and_main_keyboard, get_share_keyboard, get_black_menu
)
from keyboards.back_buttons import get_back_keyboard
from states.user_states import BlackStates
from config import LINKS, PARTNER_LINKS
import database

router = Router()


@router.callback_query(F.data == "black_problem_fees")
async def black_problem_fees(callback: CallbackQuery, state: FSMContext):
    """Выбрана проблема: комиссии"""
    user_id = callback.from_user.id
    database.update_funnel(user_id, "black", "problem_fees")

    await state.update_data(problem="fees")
    await state.set_state(BlackStates.categories)
    await callback.message.edit_text(
        "Понял! Комиссии — это больно 💸\n\n"
        "Какие у тебя главные категории трат?",
        reply_markup=get_categories_menu()
    )


@router.callback_query(F.data == "black_problem_cashback")
async def black_problem_cashback(callback: CallbackQuery, state: FSMContext):
    """Выбрана проблема: низкий кэшбэк"""
    user_id = callback.from_user.id
    database.update_funnel(user_id, "black", "problem_cashback")

    await state.update_data(problem="cashback")
    await state.set_state(BlackStates.categories)
    await callback.message.edit_text(
        "Низкий кэшбэк — это обидно! 😤\n\n"
        "Какие у тебя главные категории трат?",
        reply_markup=get_categories_menu()
    )


@router.callback_query(F.data == "black_problem_percent")
async def black_problem_percent(callback: CallbackQuery, state: FSMContext):
    """Выбрана проблема: нет % на остаток"""
    user_id = callback.from_user.id
    database.update_funnel(user_id, "black", "problem_percent")

    await state.update_data(problem="percent")
    await state.set_state(BlackStates.categories)
    await callback.message.edit_text(
        "Проценты на остаток — важная фишка! 📊\n\n"
        "Какие у тебя главные категории трат?",
        reply_markup=get_categories_menu()
    )


@router.callback_query(BlackStates.categories)
async def black_categories(callback: CallbackQuery, state: FSMContext):
    """Выбор категории трат"""
    user_id = callback.from_user.id
    category_map = {
        "black_cat_supermarkets": "супермаркеты",
        "black_cat_gas": "АЗС",
        "black_cat_travel": "путешествия",
        "black_cat_all": "всё подряд",
    }
    category = category_map.get(callback.data, "всё подряд")
    database.update_funnel(user_id, "black", f"category:{category}")

    await state.update_data(categories=category)
    await state.set_state(BlackStates.expenses)
    await callback.message.edit_text(
        f"Отлично! Категория: {category} 📝\n\n"
        "Какие у тебя траты в месяц?",
        reply_markup=get_expenses_menu()
    )


@router.callback_query(BlackStates.expenses)
async def black_expenses(callback: CallbackQuery, state: FSMContext):
    """Выбор суммы трат"""
    user_id = callback.from_user.id
    expense_map = {
        "black_exp_up20": "до 20к",
        "black_exp_20_50": "20-50к",
        "black_exp_50_100": "50-100к",
        "black_exp_100plus": "100к+",
    }
    expenses = expense_map.get(callback.data, "20-50к")
    database.update_funnel(user_id, "black", f"expenses:{expenses}")

    await state.update_data(expenses=expenses)
    await state.set_state(BlackStates.savings)
    await callback.message.edit_text(
        f"Понял, траты: {expenses} ₽\n\n"
        "Есть ли у тебя сбережения?",
        reply_markup=get_savings_menu()
    )


@router.callback_query(BlackStates.savings)
async def black_savings(callback: CallbackQuery, state: FSMContext):
    """Финал ветки Black - рекомендация"""
    user_id = callback.from_user.id
    savings = "да" if callback.data == "black_savings_yes" else "нет"
    user_data = await state.get_data()

    await state.clear()

    # Завершаем воронку
    database.complete_funnel(user_id, "black")

    # Используем партнёрскую ссылку
    partner_link = PARTNER_LINKS["black"]
    
    # Логируем конверсию (переход по ссылке)
    database.log_conversion(user_id, "black", partner_link)

    problem_text = {
        "fees": "без комиссий",
        "cashback": "с максимальным кэшбэком",
        "percent": "с процентами на остаток",
    }

    await callback.message.edit_text(
        f"🎯 <b>Тебе идеально подойдёт Tinkoff Black!</b>\n\n"
        f"✅ Кэшбэк до 30% у партнёров\n"
        f"✅ До 15% в выбранных категориях ({user_data.get('categories', 'всё подряд')})\n"
        f"✅ Бесплатное обслуживание навсегда\n"
        f"✅ % на остаток по счёту\n"
        f"✅ Без скрытых комиссий\n\n"
        f"Траты {user_data.get('expenses', '20-50к')} ₽ — это отличный повод начать получать больше!\n\n"
        f"👉 <a href='{partner_link}'>Оформить карту</a>",
        reply_markup=get_share_keyboard(),
        disable_web_page_preview=True
    )


@router.callback_query(F.data == "back_black_categories")
async def back_black_categories(callback: CallbackQuery, state: FSMContext):
    """Назад из категорий к выбору проблемы"""
    await state.set_state(None)
    await callback.message.edit_text(
        "💳 <b>Tinkoff Black</b> — карта с максимальным кэшбэком!\n\n"
        "Что бесит больше всего?",
        reply_markup=get_black_menu()
    )


@router.callback_query(F.data == "back_black_expenses")
async def back_black_expenses(callback: CallbackQuery, state: FSMContext):
    """Назад из трат к категориям"""
    await state.set_state(BlackStates.categories)
    await callback.message.edit_text(
        "Возвращаемся к выбору категорий.\n\n"
        "Какие у тебя главные категории трат?",
        reply_markup=get_categories_menu()
    )


@router.callback_query(F.data == "back_black_savings")
async def back_black_savings(callback: CallbackQuery, state: FSMContext):
    """Назад из сбережений к тратам"""
    await state.set_state(BlackStates.expenses)
    await callback.message.edit_text(
        "Возвращаемся к вопросу о тратах.\n\n"
        "Какие у тебя траты в месяц?",
        reply_markup=get_expenses_menu()
    )
