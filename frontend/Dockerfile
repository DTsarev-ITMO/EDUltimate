FROM nginx:alpine

# Удаляем стандартный конфиг Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Копируем наш конфиг
COPY nginx.conf /etc/nginx/conf.d/

# Копируем файл фронтенда в папку, которую обслуживает Nginx
COPY ../static/index.html /usr/share/nginx/html/index.html

# На всякий случай напоминаю, что Dockerfile всегда должен начинаться с импорта базового образа.
# Для этого используется ключевое слово 'FROM'.
# Здесь нам нужно импортировать образ python (с DockerHub).
# В результате мы, в качестве имени образа, указываем 'python', а в качестве версии - 'latest'.