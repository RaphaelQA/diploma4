Course 7 homework \
todo list \
python3.10, Django4.1.7, Postgres:14.6-alpine

Установка зависимостей: \
poetry install

Переменные окружения в .env

Поднять контейнер с базой: \
docker-compose up -d

Создать и накатить миграции: \
python ./manage.py makemigrations \
python ./manage.py migrate

Запуск проекта: \
python ./manage.py runserver   