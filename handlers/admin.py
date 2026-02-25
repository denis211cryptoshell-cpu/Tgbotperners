"""
Админ-панель для управления ботом и просмотра статистики
"""

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID
import database

router = Router()


def is_admin(user_id: int) -> bool:
    """Проверяет, является ли пользователь админом"""
    if not ADMIN_ID:
        return False
    return str(user_id) == str(ADMIN_ID)


class MailingStates(StatesGroup):
    """Состояния для рассылки"""
    waiting_for_message = State()


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Админ-панель - главная"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Доступ запрещён")
        return

    # Получаем статистику
    total_users = database.get_users_count()
    active_users_7d = database.get_active_users(7)
    total_conversions = database.get_total_conversions()
    conversion_stats = database.get_conversion_stats()
    funnel_stats = database.get_funnel_stats()

    # Формируем отчёт
    report = [
        f"📊 <b>Статистика бота</b>\n\n"
        f"👥 <b>Пользователи:</b>\n"
        f"   • Всего: {total_users}\n"
        f"   • Активных за 7 дней: {active_users_7d}\n\n"
        f"🎯 <b>Конверсии (переходы по ссылкам):</b>\n"
        f"   • Всего: {total_conversions}\n"
    ]

    # Добавляем статистику по продуктам
    if conversion_stats:
        report.append("\n📈 <b>По продуктам:</b>")
        for product, clicks in conversion_stats.items():
            emoji = {
                "black": "💳",
                "credit_card": "💰",
                "investment": "📈",
                "t_mobile": "📱",
                "insurance": "🛡"
            }.get(product, "•")
            report.append(f"   {emoji} {product}: {clicks}")

    # Добавляем статистику по воронкам
    if funnel_stats:
        report.append("\n🔄 <b>Воронки:</b>")
        for funnel in funnel_stats:
            total = funnel['total']
            completed = funnel['completed'] or 0
            conversion_rate = round(completed / total * 100, 1) if total > 0 else 0
            report.append(
                f"   • {funnel['funnel_type']}: "
                f"{completed}/{total} ({conversion_rate}%)"
            )

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text="📥 Экспорт пользователей (CSV)",
            callback_data="admin_export_users"
        )],
        [types.InlineKeyboardButton(
            text="🔄 Обновить",
            callback_data="admin_refresh"
        )],
    ])

    await message.answer("\n".join(report), reply_markup=keyboard)


@router.callback_query(F.data == "admin_refresh")
async def admin_refresh(callback: CallbackQuery):
    """Обновление статистики"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Доступ запрещён", show_alert=True)
        return

    # Удаляем старое сообщение и отправляем новое
    await callback.message.delete()
    # Создаём фейковое сообщение для cmd_admin
    fake_message = types.Message(
        message_id=0,
        date=callback.message.date,
        chat=callback.message.chat,
        from_user=callback.from_user
    )
    await cmd_admin(fake_message)


@router.callback_query(F.data == "admin_export_users")
async def admin_export_users(callback: CallbackQuery):
    """Экспорт всех пользователей в CSV"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Доступ запрещён", show_alert=True)
        return

    users = database.get_all_users()

    if not users:
        await callback.answer("❌ Нет пользователей для экспорта", show_alert=True)
        return

    # Формируем CSV
    csv_content = "user_id,username,first_name,last_name,created_at,last_seen_at\n"
    for user in users:
        csv_content += (
            f"{user['user_id']},"
            f"{user['username'] or ''},"
            f"{user['first_name'] or ''},"
            f"{user['last_name'] or ''},"
            f"{user['created_at']},"
            f"{user['last_seen_at']}\n"
        )

    # Отправляем файл
    file = types.BufferedInputFile(
        csv_content.encode('utf-8'),
        filename=f"users_export_{len(users)}.csv"
    )

    await callback.message.answer_document(
        document=file,
        caption=f"📥 Экспортировано {len(users)} пользователей"
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    """Отмена текущего действия"""
    await state.clear()
    await message.answer("❌ Действие отменено")
