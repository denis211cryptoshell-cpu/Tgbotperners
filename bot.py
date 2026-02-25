import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from handlers import start, black, credit_card, investments, other
from middleware import subscription

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрация роутеров
dp.include_router(start.router)
dp.include_router(black.router)
dp.include_router(credit_card.router)
dp.include_router(investments.router)
dp.include_router(other.router)


async def main():
    """Запуск бота"""
    logging.info("Бот запускается...")
    
    # Удаляем вебхук (на случай если был установлен)
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Запуск polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен")
