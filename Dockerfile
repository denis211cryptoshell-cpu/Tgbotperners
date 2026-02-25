# Используем легкий образ Python
FROM python:3.12-slim

# Рабочая директория
WORKDIR /app

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаём директорию для базы данных
RUN mkdir -p /app/data

# Запускаем бота
CMD ["python", "bot.py"]
