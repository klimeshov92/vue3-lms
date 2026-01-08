# Базовый образ с Python
FROM python:3.11-slim

# Отключаем .pyc файлы
ENV PYTHONDONTWRITEBYTECODE=1
# Логи сразу в stdout
ENV PYTHONUNBUFFERED=1

# Рабочая директория контейнера
WORKDIR /app

# Системные зависимости для Python и PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Явно указываем порт (документация + порядок)
EXPOSE 8000

# Запуск Django через Gunicorn + Uvicorn
# 2 воркера — оптимально для REST + WebSocket
CMD ["gunicorn", "light.asgi:application", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "-w", "2", \
     "-b", "0.0.0.0:8000"]

