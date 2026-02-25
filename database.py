"""
База данных для Telegram бота
Хранит пользователей, статистику и переходы по ссылкам
"""

import sqlite3
from datetime import datetime
from contextlib import contextmanager


# Путь к файлу базы данных
DATABASE_PATH = "bot_database.db"


@contextmanager
def get_connection():
    """Менеджер контекста для подключения к БД"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Чтобы получать строки как словари
    try:
        yield conn
    finally:
        conn.close()


def init_database():
    """Создаёт таблицы базы данных при первом запуске"""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                language_code TEXT,
                is_bot BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Таблица статистики действий (какие кнопки нажимали)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action_type TEXT,
                action_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Таблица переходов по ссылкам (конверсии)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_type TEXT,
                link_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Таблица воронок (на каком этапе воронки пользователь)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS funnels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                funnel_type TEXT,
                stage TEXT,
                stage_data TEXT,
                completed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Таблица для админских рассылок
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mailings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_text TEXT,
                total_users INTEGER,
                sent_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        """)
        
        conn.commit()


# === Функции для работы с пользователями ===

def add_or_update_user(user_id: int, username: str = None, first_name: str = None,
                       last_name: str = None, language_code: str = None, is_bot: bool = False):
    """Добавляет нового пользователя или обновляет данные существующего"""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Проверяем, есть ли пользователь
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        exists = cursor.fetchone()
        
        if exists:
            # Обновляем last_seen_at и данные
            cursor.execute("""
                UPDATE users 
                SET username = ?, first_name = ?, last_name = ?, 
                    language_code = ?, last_seen_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (username, first_name, last_name, language_code, user_id))
        else:
            # Добавляем нового
            cursor.execute("""
                INSERT INTO users (user_id, username, first_name, last_name, language_code, is_bot)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, username, first_name, last_name, language_code, is_bot))
        
        conn.commit()


def get_user(user_id: int) -> dict:
    """Получает данные пользователя по ID"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_all_users() -> list:
    """Получает всех пользователей"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]


def get_users_count() -> int:
    """Получает общее количество пользователей"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM users")
        return cursor.fetchone()["count"]


def get_active_users(days: int = 7) -> int:
    """Получает количество активных пользователей за последние N дней"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as count FROM users 
            WHERE last_seen_at >= datetime('now', ?)
        """, (f'-{days} days',))
        return cursor.fetchone()["count"]


# === Функции для работы с действиями (статистика кнопок) ===

def log_action(user_id: int, action_type: str, action_data: str = None):
    """Записывает действие пользователя (нажатие кнопки, команда)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO actions (user_id, action_type, action_data)
            VALUES (?, ?, ?)
        """, (user_id, action_type, action_data))
        conn.commit()


def get_action_stats() -> dict:
    """Получает статистику по действиям (какие кнопки популярны)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT action_type, action_data, COUNT(*) as count
            FROM actions
            GROUP BY action_type, action_data
            ORDER BY count DESC
        """)
        return [dict(row) for row in cursor.fetchall()]


def get_user_actions(user_id: int, limit: int = 50) -> list:
    """Получает последние действия пользователя"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM actions 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (user_id, limit))
        return [dict(row) for row in cursor.fetchall()]


# === Функции для работы с конверсиями (переходы по ссылкам) ===

def log_conversion(user_id: int, product_type: str, link_url: str):
    """Записывает переход по ссылке (конверсия)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO conversions (user_id, product_type, link_url)
            VALUES (?, ?, ?)
        """, (user_id, product_type, link_url))
        conn.commit()


def get_conversion_stats() -> dict:
    """Получает статистику по продуктам (сколько кликов на каждый продукт)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product_type, COUNT(*) as clicks
            FROM conversions
            GROUP BY product_type
            ORDER BY clicks DESC
        """)
        return {row["product_type"]: row["clicks"] for row in cursor.fetchall()}


def get_total_conversions() -> int:
    """Получает общее количество переходов по ссылкам"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM conversions")
        return cursor.fetchone()["count"]


# === Функции для работы с воронками ===

def start_funnel(user_id: int, funnel_type: str):
    """Начинает новую воронку для пользователя"""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Завершаем предыдущие незавершённые воронки этого типа
        cursor.execute("""
            UPDATE funnels 
            SET completed = -1 
            WHERE user_id = ? AND funnel_type = ? AND completed = 0
        """, (user_id, funnel_type))
        
        # Создаём новую
        cursor.execute("""
            INSERT INTO funnels (user_id, funnel_type, stage, stage_data, completed)
            VALUES (?, ?, '', '', 0)
        """, (user_id, funnel_type))
        conn.commit()


def update_funnel(user_id: int, funnel_type: str, stage: str, stage_data: str = None):
    """Обновляет этап воронки"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE funnels 
            SET stage = ?, stage_data = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ? AND funnel_type = ? AND completed = 0
        """, (stage, stage_data, user_id, funnel_type))
        conn.commit()


def complete_funnel(user_id: int, funnel_type: str):
    """Завершает воронку успешно"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE funnels 
            SET completed = 1, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ? AND funnel_type = ? AND completed = 0
        """, (user_id, funnel_type))
        conn.commit()


def get_funnel_stats() -> list:
    """Получает статистику по воронкам (сколько дошло до конца)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                funnel_type,
                COUNT(*) as total,
                SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN completed = 0 THEN 1 ELSE 0 END) as in_progress,
                SUM(CASE WHEN completed = -1 THEN 1 ELSE 0 END) as abandoned
            FROM funnels
            GROUP BY funnel_type
        """)
        return [dict(row) for row in cursor.fetchall()]


# === Функции для админских рассылок ===

def add_mailing(message_text: str, total_users: int):
    """Добавляет запись о рассылке"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO mailings (message_text, total_users)
            VALUES (?, ?)
        """, (message_text, total_users))
        conn.commit()
        return cursor.lastrowid


def update_mailing_sent(mailing_id: int, sent_count: int):
    """Обновляет количество отправленных сообщений в рассылке"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE mailings 
            SET sent_count = ?, completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (sent_count, mailing_id))
        conn.commit()


def get_mailing_stats() -> list:
    """Получает статистику по рассылкам"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM mailings ORDER BY created_at DESC LIMIT 10
        """)
        return [dict(row) for row in cursor.fetchall()]


# Инициализация БД при импорте (создаст файл если нет)
init_database()
