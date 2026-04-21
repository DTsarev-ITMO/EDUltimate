# Используем легкий образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /frontend

# Копируем index.html (и другие файлы, если есть) в контейнер
COPY . .

## Указываем значение FRONT_PORT по умолчанию, если переменная не будет передана
ENV FRONT_PORT=5500

## Используем shell-форму записи CMD, чтобы переменная подставилась
CMD python3 -m http.server $FRONT_PORT --bind 0.0.0.0