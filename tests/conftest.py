"""
Конфигурация для тестов
"""
import pytest


@pytest.fixture
def test_user():
    """Тестовый пользователь"""
    return {
        "user_id": 123456789,
        "username": "test_user",
        "first_name": "Test",
        "last_name": "User",
        "language_code": "ru",
        "is_bot": False
    }


@pytest.fixture
def mock_bot(mocker):
    """Моковый бот"""
    bot = mocker.Mock()
    return bot
