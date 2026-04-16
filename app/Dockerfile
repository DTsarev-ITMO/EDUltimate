# Используем легкий образ Python
FROM python:3.11-slim

# Устанавливаем системные зависимости для работы PostgreSQL (psycopg2)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app/backend

# Отключаем создание .pyc файлов и включаем буферизацию логов
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Сначала копируем только requirements, чтобы закэшировать установку библиотек
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код проекта
COPY app .

# Команда для запуска (uvicorn)
# Используем 0.0.0.0, чтобы сервер был доступен снаружи контейнера
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
