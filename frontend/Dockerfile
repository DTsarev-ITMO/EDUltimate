FROM cr.yandex/mirror/library/python:3.11-slim

# Переключаем репозитории на зеркала Yandex
RUN sed -i 's/deb.debian.org/mirror.yandex.ru/g' /etc/apt/sources.list.d/debian.sources || true
RUN sed -i 's/security.debian.org/mirror.yandex.ru/g' /etc/apt/sources.list.d/debian.sources || true

# Установим curl для healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /frontend
COPY . .

ENV FRONT_PORT=5500
CMD python3 -m http.server $FRONT_PORT --bind 0.0.0.0