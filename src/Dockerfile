# Используем легкий образ Python
FROM python:3.11-slim

# Устанавливаем системные зависимости для работы PostgreSQL (psycopg2)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Установим curl, для healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /src

# Отключаем создание .pyc файлов и включаем буферизацию логов
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Сначала копируем только requirements, чтобы закэшировать установку библиотек
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код проекта
COPY . .

# Команда для запуска (uvicorn)
CMD alembic upgrade head && uvicorn app.main:app --host $BACKEND_IP --port $BACKEND_PORT --reload &
