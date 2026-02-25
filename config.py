import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv(override=True)

# Токен бота от @BotFather
TOKEN = os.getenv("TOKEN", "YOUR_BOT_TOKEN_HERE")

# Ссылки на продукты Т-Банка
LINKS = {
    "black": "https://www.tbank.ru/tinkoff-black/",
    "credit_card": "https://www.tbank.ru/credit-card/",
    "investments": "https://www.tbank.ru/invest/",
    "t_mobile": "https://www.tbank.ru/mobile/",
    "insurance": "https://www.tbank.ru/insurance/",
}

# Партнёрские ссылки (CPA)
PARTNER_LINKS = {
    "black": "https://t-cpa.ru/2t7CAG",  # Твоя партнёрская ссылка на Black
    "credit_card": "https://www.tbank.ru/credit-card/",  # Замените на партнёрскую
    "investments": "https://www.tbank.ru/invest/",  # Замените на партнёрскую
}

# ID админа для логирования (опционально)
ADMIN_ID = os.getenv("ADMIN_ID")

# Канал для проверки подписки
CHANNEL_ID = "@tbankacess"  # username канала
CHANNEL_LINK = "https://t.me/tbankacess"  # ссылка для подписки
