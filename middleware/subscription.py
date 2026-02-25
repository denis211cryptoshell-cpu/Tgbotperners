from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from config import CHANNEL_ID, CHANNEL_LINK
from keyboards.main_menu import get_main_menu
import database


class IsSubscribedFilter(BaseFilter):
    """Фильтр для проверки подписки на канал"""
    
    async def __call__(self, event: Message | CallbackQuery, bot) -> bool:
        # Получаем user_id из сообщения или callback query
        if isinstance(event, Message):
            user_id = event.from_user.id
        else:
            user_id = event.from_user.id
        
        try:
            # Проверяем статус участника в канале
            member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
            # Подписан если статус не left и не kicked
            return member.status in ["member", "administrator", "creator"]
        except Exception:
            # Если ошибка (например, бот не админ в канале) - пропускаем
            return True


async def check_subscription(message: Message | CallbackQuery, bot) -> bool:
    """Проверка подписки с отправкой сообщения если не подписан"""
    if isinstance(message, CallbackQuery):
        user_id = message.from_user.id
        send_message = message.message.answer
    else:
        user_id = message.from_user.id
        send_message = message.answer

    # Сохраняем пользователя в БД
    database.add_or_update_user(
        user_id=user_id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        language_code=message.from_user.language_code,
        is_bot=message.from_user.is_bot
    )

    # Логируем действие
    if isinstance(message, CallbackQuery):
        database.log_action(user_id, "callback", message.data)
    else:
        cmd = message.text.split()[0] if message.text and message.text.startswith('/') else "message"
        database.log_action(user_id, "command" if message.text and message.text.startswith('/') else "message", cmd)

    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
    except Exception:
        # Если ошибка - пропускаем пользователя
        return True

    # Пользователь не подписан
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="✅ Подписаться на канал",
            url=CHANNEL_LINK
        )],
        [InlineKeyboardButton(
            text="🔄 Я подписался, проверить",
            callback_data="check_subscription"
        )],
    ])

    await send_message(
        "⚠️ <b>Доступ ограничен!</b>\n\n"
        "Для использования бота необходимо подписаться на наш канал:\n"
        f"👉 <a href='{CHANNEL_LINK}'>@tbankacess</a>\n\n"
        "После подписки нажмите кнопку «Я подписался, проверить»:",
        reply_markup=keyboard
    )

    return False


async def process_check_subscription(callback: CallbackQuery, bot):
    """Обработчик кнопки проверки подписки"""
    user_id = callback.from_user.id
    
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            await callback.message.edit_text(
                "✅ <b>Подписка подтверждена!</b>\n\n"
                "Теперь вам доступны все функции бота.\n"
                "Выберите направление:",
                reply_markup=get_main_menu()
            )
            return True
    except Exception:
        # Если ошибка - пропускаем
        await callback.message.edit_text(
            "✅ <b>Подписка подтверждена!</b>\n\n"
            "Теперь вам доступны все функции бота.\n"
            "Выберите направление:",
            reply_markup=get_main_menu()
        )
        return True
    
    await callback.answer("❌ Вы ещё не подписались на канал!", show_alert=True)
    return False
