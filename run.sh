#!/bin/sh

# 1. Собрать контейнеры и запустить их
echo "Собираем контейнеры"
sudo docker compose up -d
echo "Контейнеры запущены"

# 2. Добавляем суперадмина, если требуется
#python -m app.scripts.create_admin

# 3. Проверяем базу данных продуктов и парсим данные, если требуется
#python -m app.scripts.parse_food

# 4. Все работает, сообщаем адреса, начинаем читать логи

echo "FastAPI доступен по адресу http://localhost:8000/docs"
echo "Фронтенд доступен по адресу http://localhost:5500"
echo "Доступ к БД можно осуществить через хост localhost и порт 5433"