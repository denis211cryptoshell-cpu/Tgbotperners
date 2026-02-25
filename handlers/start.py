from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.main_menu import get_main_menu, get_back_and_main_keyboard
from middleware.subscription import check_subscription, process_check_subscription
import database

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, bot):
    """Обработчик команды /start"""
    # Проверяем подписку
    if not await check_subscription(message, bot):
        return
    
    await message.answer(
        "Привет! 😊 Устал от комиссий, низкого кэшбэка или отказов в кредите? "
        "Подберу продукт Т-Банка под твою ситуацию.\n\n"
        "Выбери, что для тебя актуально:",
        reply_markup=get_main_menu()
    )


@router.message(Command("menu"))
async def cmd_menu(message: Message, bot):
    """Обработчик команды /menu - возвращает главное меню"""
    # Проверяем подписку
    if not await check_subscription(message, bot):
        return

    await message.answer(
        "Главное меню:",
        reply_markup=get_main_menu()
    )


@router.message(Command("help"))
async def cmd_help(message: Message, bot):
    """Обработчик команды /help - справка"""
    await message.answer(
        "ℹ️ <b>Справка по боту</b>\n\n"
        "📋 <b>Доступные команды:</b>\n"
        "• /start - Запустить бота и главное меню\n"
        "• /menu - Показать главное меню\n"
        "• /help - Эта справка\n"
        "• /admin - Админ-панель (только для админа)\n\n"
        "🎯 <b>Как это работает:</b>\n"
        "1. Выберите продукт в главном меню\n"
        "2. Ответьте на несколько вопросов\n"
        "3. Получите персональную рекомендацию\n"
        "4. Перейдите по ссылке для оформления\n\n"
        "💡 <b>Совет:</b> Используйте калькулятор выгоды, "
        "чтобы узнать, сколько вы можете сэкономить!"
    )


@router.callback_query(F.data == "check_subscription")
async def check_sub_callback(callback: CallbackQuery, bot):
    """Проверка подписки после нажатия кнопки"""
    await process_check_subscription(callback, bot)


@router.callback_query(F.data == "main_menu")
async def process_main_menu(callback: CallbackQuery, bot):
    """Возврат в главное меню"""
    # Проверяем подписку
    if not await check_subscription(callback, bot):
        return
    
    await callback.message.edit_text(
        "Главное меню. Выбери направление:",
        reply_markup=get_main_menu()
    )


@router.callback_query(F.data == "back")
async def process_back(callback: CallbackQuery, bot):
    """Обработчик кнопки Назад - возвращает на шаг"""
    # Проверяем подписку
    if not await check_subscription(callback, bot):
        return
    
    await callback.message.edit_text(
        "Возврат на шаг назад. Выбери направление:",
        reply_markup=get_main_menu()
    )


@router.callback_query(F.data == "black_card")
async def process_black_card(callback: CallbackQuery, bot):
    """Начало ветки Tinkoff Black"""
    # Проверяем подписку
    if not await check_subscription(callback, bot):
        return

    from keyboards.main_menu import get_black_menu

    # Начинаем воронку Black
    database.start_funnel(callback.from_user.id, "black")
    database.update_funnel(callback.from_user.id, "black", "start")

    await callback.message.edit_text(
        "💳 <b>Tinkoff Black</b> — карта с максимальным кэшбэком!\n\n"
        "Что бесит больше всего?",
        reply_markup=get_black_menu()
    )


@router.callback_query(F.data == "credit_card")
async def process_credit_card(callback: CallbackQuery, bot):
    """Начало ветки кредитной карты"""
    # Проверяем подписку
    if not await check_subscription(callback, bot):
        return
    
    from keyboards.main_menu import get_credit_problem_menu
    
    await callback.message.edit_text(
        "💰 <b>Кредитная карта</b> — деньги в долг без процентов!\n\n"
        "Что не нравится в текущей кредитке (или почему хочешь новую)?",
        reply_markup=get_credit_problem_menu()
    )


@router.callback_query(F.data == "investments")
async def process_investments(callback: CallbackQuery, bot):
    """Начало ветки инвестиций"""
    # Проверяем подписку
    if not await check_subscription(callback, bot):
        return
    
    from keyboards.main_menu import get_invest_problem_menu
    
    await callback.message.edit_text(
        "📈 <b>Инвестиции</b> — приумножь свои сбережения!\n\n"
        "Что мешает начать инвестировать?",
        reply_markup=get_invest_problem_menu()
    )


@router.callback_query(F.data == "other_products")
async def process_other_products(callback: CallbackQuery, bot):
    """Начало ветки другие продукты"""
    # Проверяем подписку
    if not await check_subscription(callback, bot):
        return
    
    from keyboards.main_menu import get_other_menu
    
    await callback.message.edit_text(
        "📱 <b>Другие продукты</b> Т-Банка\n\n"
        "Что тебя интересует?",
        reply_markup=get_other_menu()
    )


@router.callback_query(F.data == "promo")
async def process_promo(callback: CallbackQuery, bot):
    """Ветка с акциями"""
    # Проверяем подписку
    if not await check_subscription(callback, bot):
        return
    
    await callback.message.edit_text(
        "🎁 <b>Акции Т-Банка</b>\n\n"
        "• Открой карту — получи 500 ₽\n"
        "• Приведи друга — получи 1000 ₽\n"
        "• Первая покупка в приложении — кэшбэк 10%\n\n"
        "Следи за обновлениями!",
        reply_markup=get_back_and_main_keyboard()
    )
