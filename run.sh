#!/bin/sh

# 1. Собрать контейнеры и запустить их
echo "Собираем контейнеры"
sudo docker compose up -d
echo "Контейнеры запущены"

# 2. Добавляем суперадмина, если требуется
python -m app.scripts.create_admin
echo "Суперадмин на связи"

# 3. Проверяем базу данных продуктов и парсим данные, если требуется
python -m app.scripts.parse_food
#echo "Суперадмин на связи"

echo "FastAPI доступен по адресу http://localhost:8000/docs"
echo "Фронтенд доступен по адресу http://localhost:5500"
echo "Доступ к БД можно осуществить через хост localhost и порт 5433"



## 2.
#echo "Проверяем наличие суперадмина"
#
## 1. Ожидание готовности базы данных (PostgreSQL)
#echo "Waiting for postgres..."
#while ! nc -z $DB_HOST $DB_PORT; do
#  sleep 0.1
#done
#echo "PostgreSQL started"
#
## 2. Осуществить миграцию базы данных
#echo "Running migrations..."
#alembic upgrade head
#
## 3. Добавить администратора
#echo "Creating admin user..."
#python scripts/create_admin.py
#
## 4. Осуществить парсинг данных
#echo "Parsing food data..."
#python scripts/parse_data.py
#
## 5. Запустить бэкенд
#echo "Starting FastAPI..."
#exec uvicorn app.main:app --host 0.0.0.0 --port 8000
