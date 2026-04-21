#!/bin/sh

# 1. Собрать контейнеры и запустить их
echo "Собираем контейнеры"
sudo docker compose up -d
echo "Контейнеры запущены"


# 2. Ждем, пока API станет доступно
echo "Ожидаем запуска API..."
# Цикл проверяет код ответа 200 от вашего API (например, эндпоинт документации или healthcheck)
until $(curl -output /dev/null --silent --head --fail http://localhost:8000/docs); do
    printf '.'
    sleep 2
done
echo "API запущено!"

# 2. Добавляем суперадмина, если требуется
python -m app.scripts.create_admin

# 3. Проверяем базу данных продуктов и парсим данные, если требуется
python -m app.scripts.parse_food

# 4. Все работает, сообщаем адреса, начинаем читать логи

echo "FastAPI доступен по адресу http://localhost:8000/docs"
echo "Фронтенд доступен по адресу http://localhost:5500"
echo "Доступ к БД можно осуществить через хост localhost и порт 5433"