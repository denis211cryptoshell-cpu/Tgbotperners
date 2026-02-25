"""
Хендлеры для калькулятора кэшбэка
Помогает пользователю посчитать потенциальный кэшбэк с Tinkoff Black
"""

from aiogram import Router, F, types
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.main_menu import get_back_and_main_keyboard
import database

router = Router()


class CashbackStates(StatesGroup):
    """Состояния для калькулятора кэшбэка"""
    waiting_for_expenses = State()


@router.callback_query(F.data == "cashback_calculator")
async def cashback_calculator_start(callback: CallbackQuery):
    """Запуск калькулятора кэшбэка"""
    user_id = callback.from_user.id
    
    # Логируем действие
    database.log_action(user_id, "calculator", "cashback_start")
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text="💳 Обычная карта (1%)",
            callback_data="cashback_compare_standard"
        )],
        [types.InlineKeyboardButton(
            text="🔥 Tinkoff Black (до 15%)",
            callback_data="cashback_compare_black"
        )],
        [types.InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="back"
        )],
    ])
    
    await callback.message.edit_text(
        "🧮 <b>Калькулятор кэшбэка</b>\n\n"
        "Давайте посчитаем, сколько вы можете получать с кэшбэка!\n\n"
        "Введите ваши средние траты в месяц (числом, без пробелов):\n"
        "Например: 25000",
        reply_markup=keyboard
    )


@router.callback_query(F.data.startswith("cashback_compare_"))
async def cashback_compare(callback: CallbackQuery):
    """Сравнение кэшбэка"""
    user_id = callback.from_user.id
    card_type = callback.data.split("_")[-1]
    
    database.log_action(user_id, "calculator", f"cashback_compare_{card_type}")
    
    # Примерные расчёты для разных сумм
    examples = {
        20000: {"standard": 200, "black": 2000},
        50000: {"standard": 500, "black": 5000},
        100000: {"standard": 1000, "black": 10000},
    }
    
    report = "📊 <b>Сравнение кэшбэка</b>\n\n"
    report += "При обычных ставках:\n"
    report += "• Стандартная карта: 1% на всё\n"
    report += "• Tinkoff Black: до 15% в категориях + 1% на остальное\n\n"
    
    for expenses, cashbacks in examples.items():
        if card_type == "standard":
            report += f"Траты {expenses:,} ₽ → кэшбэк ~{cashbacks['standard']:,} ₽\n"
        else:
            report += f"Траты {expenses:,} ₽ → кэшбэк до {cashbacks['black']:,} ₽\n"
    
    report += "\n💡 <b>Вывод:</b> С Tinkoff Black вы можете получать в 10 раз больше!\n"
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text="📝 Посчитать мои траты",
            callback_data="cashback_my_expenses"
        )],
        [types.InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="cashback_calculator"
        )],
    ])
    
    await callback.message.edit_text(report, reply_markup=keyboard)


@router.callback_query(F.data == "cashback_my_expenses")
async def cashback_my_expenses(callback: CallbackQuery, state: FSMContext):
    """Ввод своих трат для расчёта"""
    await state.set_state(CashbackStates.waiting_for_expenses)
    
    await callback.message.edit_text(
        "💰 <b>Расчёт кэшбэка</b>\n\n"
        "Введите ваши средние месячные траты (числом):\n\n"
        "Или отправьте /cancel для отмены"
    )


@router.message(CashbackStates.waiting_for_expenses)
async def cashback_calculate(message: Message, state: FSMContext):
    """Расчёт кэшбэка"""
    try:
        expenses = int(message.text.replace(" ", "").replace("₽", "").replace("руб", ""))
    except ValueError:
        await message.answer(
            "❌ Пожалуйста, введите число (например: 25000)\n\n"
            "Или /cancel для отмены"
        )
        return
    
    # Считаем кэшбэк
    # Стандартная карта: 1%
    standard_cashback = expenses * 0.01
    
    # Tinkoff Black: предполагаем, что 50% трат в категориях с 15%, остальное с 1%
    black_cashback = (expenses * 0.5 * 0.15) + (expenses * 0.5 * 0.01)
    
    # Разница
    difference = black_cashback - standard_cashback
    
    # Годовой кэшбэк
    yearly_standard = standard_cashback * 12
    yearly_black = black_cashback * 12
    yearly_diff = difference * 12
    
    result = (
        f"📊 <b>Ваш персональный расчёт</b>\n\n"
        f"Траты в месяц: {expenses:,} ₽\n\n"
        f"💳 <b>Стандартная карта (1%):</b>\n"
        f"   • В месяц: {standard_cashback:,.0f} ₽\n"
        f"   • В год: {yearly_standard:,.0f} ₽\n\n"
        f"🔥 <b>Tinkoff Black (до 15%):</b>\n"
        f"   • В месяц: {black_cashback:,.0f} ₽\n"
        f"   • В год: {yearly_black:,.0f} ₽\n\n"
        f"💰 <b>Ваша выгода:</b>\n"
        f"   • В месяц: +{difference:,.0f} ₽\n"
        f"   • В год: +{yearly_diff:,.0f} ₽\n\n"
        f"⚡ Tinkoff Black выгоднее в {black_cashback/standard_cashback:.1f} раз!"
        if standard_cashback > 0 else "⚡ Tinkoff Black выгоднее!"
    )
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text="👉 Оформить карту",
            url="https://www.tbank.ru/tinkoff-black/"
        )],
        [types.InlineKeyboardButton(
            text="🔄 Посчитать ещё раз",
            callback_data="cashback_calculator"
        )],
    ])
    
    await state.clear()
    
    # Логируем
    database.log_action(message.from_user.id, "calculator", f"cashback_calculated:{expenses}")
    
    await message.answer(result, reply_markup=keyboard)


@router.callback_query(F.data == "calculator_menu")
async def calculator_menu(callback: CallbackQuery):
    """Меню калькуляторов"""
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text="🧮 Калькулятор кэшбэка",
            callback_data="cashback_calculator"
        )],
        [types.InlineKeyboardButton(
            text="💰 Калькулятор кредита",
            callback_data="credit_calculator"  # Можно добавить позже
        )],
        [types.InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="main_menu"
        )],
    ])
    
    await callback.message.edit_text(
        "🧮 <b>Калькуляторы Т-Банка</b>\n\n"
        "Выберите, что хотите рассчитать:",
        reply_markup=keyboard
    )
