"""
Тесты для базы данных
"""
import pytest
import database
import os


class TestDatabase:
    """Тесты для функций базы данных"""

    def test_add_or_update_user(self, test_user):
        """Тест добавления пользователя"""
        # Добавляем пользователя
        database.add_or_update_user(**test_user)
        
        # Получаем и проверяем
        user = database.get_user(test_user["user_id"])
        assert user is not None
        assert user["username"] == test_user["username"]
        assert user["first_name"] == test_user["first_name"]

    def test_get_users_count(self):
        """Тест подсчёта пользователей"""
        count = database.get_users_count()
        assert count >= 0  # Должно быть неотрицательное число

    def test_log_action(self, test_user):
        """Тест логирования действий"""
        # Сначала добавим пользователя (если нет)
        database.add_or_update_user(**test_user)
        
        # Логируем действие
        database.log_action(test_user["user_id"], "test_action", "test_data")
        
        # Получаем действия
        actions = database.get_user_actions(test_user["user_id"], limit=10)
        assert len(actions) > 0
        assert actions[0]["action_type"] == "test_action"

    def test_log_conversion(self, test_user):
        """Тест логирования конверсий"""
        database.add_or_update_user(**test_user)
        
        # Логируем конверсию
        database.log_conversion(
            test_user["user_id"],
            "test_product",
            "https://example.com"
        )
        
        # Получаем статистику
        stats = database.get_conversion_stats()
        assert "test_product" in stats or len(stats) > 0

    def test_funnel_workflow(self, test_user):
        """Тест работы с воронками"""
        database.add_or_update_user(**test_user)
        
        user_id = test_user["user_id"]
        funnel_type = "test_funnel"
        
        # Начинаем воронку
        database.start_funnel(user_id, funnel_type)
        
        # Обновляем этап
        database.update_funnel(user_id, funnel_type, "stage1", "data1")
        
        # Завершаем
        database.complete_funnel(user_id, funnel_type)
        
        # Проверяем статистику
        stats = database.get_funnel_stats()
        test_funnel = next(
            (f for f in stats if f["funnel_type"] == funnel_type),
            None
        )
        assert test_funnel is not None
        assert test_funnel["completed"] >= 1

    def test_get_active_users(self):
        """Тест получения активных пользователей"""
        count = database.get_active_users(days=7)
        assert count >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
