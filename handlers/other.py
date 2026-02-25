from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.main_menu import get_other_menu, get_back_and_main_keyboard, get_share_keyboard
from states.user_states import OtherStates
from config import LINKS
import database

router = Router()


@router.callback_query(F.data == "other_tmobile")
async def other_tmobile(callback: CallbackQuery, state: FSMContext):
    """Ветка T-Mobile"""
    user_id = callback.from_user.id
    
    # Начинаем воронку
    database.start_funnel(user_id, "other")
    database.update_funnel(user_id, "other", "tmobile")
    
    await state.set_state(OtherStates.choice)
    await state.update_data(choice="tmobile")
    await callback.message.edit_text(
        "📱 <b>T-Mobile</b> — мобильная связь от Т-Банка!\n\n"
        "Всего 390 ₽/мес за:\n"
        "✅ Безлимитные мессенджеры\n"
        "✅ 10 ГБ интернета\n"
        "✅ Бесплатные звонки по России\n"
        "✅ Кэшбэк 1% рублями\n\n"
        "Хочешь оформить?",
        reply_markup=get_share_keyboard()
    )


@router.callback_query(F.data == "other_insurance")
async def other_insurance(callback: CallbackQuery, state: FSMContext):
    """Ветка страхования"""
    user_id = callback.from_user.id
    
    # Обновляем воронку
    database.update_funnel(user_id, "other", "insurance")
    
    await state.set_state(OtherStates.choice)
    await state.update_data(choice="insurance")
    await callback.message.edit_text(
        "🛡 <b>Страхование от Т-Банка</b>\n\n"
        "Выбери тип страхования:\n\n"
        "• 🏥 Здоровье — от 990 ₽/мес\n"
        "• 🏠 Имущество — от 590 ₽/мес\n"
        "• 🚗 Авто — от 1490 ₽/мес\n"
        "• ✈️ Путешествия — от 150 ₽/выезд\n\n"
        "Все полисы оформляются онлайн за 5 минут!",
        reply_markup=get_share_keyboard()
    )


@router.callback_query(F.data == "other_details")
async def other_details(callback: CallbackQuery, state: FSMContext):
    """Детали запроса"""
    user_id = callback.from_user.id
    user_data = await state.get_data()
    choice = user_data.get('choice', 'tmobile')

    await state.clear()

    # Завершаем воронку и логируем конверсию
    database.complete_funnel(user_id, "other")
    
    if choice == "tmobile":
        database.log_conversion(user_id, "t_mobile", LINKS["t_mobile"])
        await callback.message.edit_text(
            "📱 <b>Оформление T-Mobile</b>\n\n"
            "Переходи по ссылке и оформи SIM-карту:\n"
            f"👉 <a href='{LINKS['t_mobile']}'>T-Mobile</a>\n\n"
            "Используй промокод TGPARTNER для скидки 10%!",
            reply_markup=get_share_keyboard(),
            disable_web_page_preview=True
        )
    else:
        database.log_conversion(user_id, "insurance", LINKS["insurance"])
        await callback.message.edit_text(
            "🛡 <b>Оформление страхования</b>\n\n"
            "Переходи по ссылке и выбери нужный полис:\n"
            f"👉 <a href='{LINKS['insurance']}'>Страхование</a>\n\n"
            "Используй промокод TGPARTNER для скидки 5%!",
            reply_markup=get_share_keyboard(),
            disable_web_page_preview=True
        )
