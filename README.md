# YaMDb

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

## Приступая к работе

    После выполнения всех действий на вашем компьютере в двух docker-контейнерах будет развёрнут проект YaMDb.
Образ для первого контейнера собирается из директории infra_sp2 при помощи Dockerfile. Второй образ (postgres) берётся с Docker Hub.
    Клонируйте репозиторий себе на компьютер.
    Для запуска необходимо выполнить из директории с проектом команду:

```
docker-compose up
```

*Все миграции применяются автоматически при создании контейнера web*

    **Создание суперпользователя:**
Зайдите в контейнер web:
    
```
docker exec -it <CONTAINER ID> bash
```
Выполните команду
    
```
python manage.py createsuperuser --username <ADMIN NAME>
```

    **Заполнение базы тестовыми данными:**
Для заполнения базы тестовыми данными вы можете использовать файл fixtures.json, который находится в infra_sp2.
В контейнере web выполните

```
python manage.py loaddata fixtures.json
```
## Работа с базой произведений
    В данном проекте добавлять, изменять и удалять произведения, жанры и категории имеет право только администратор.
Данные действия можно произвести через панель управления

```
http://127.0.0.1:8000/admin
```

## Регистрация и оставление отзыва

    **Регистрация на YaMBd нового пользователя:**
Отправьте POST запрос с указанием вашего email
```
POST   http://127.0.0.1:8000/api/v1/auth/email/
Content-Type: application/json

{
    "email": "<EMAIL>"
}
```

В ответ вы получите код подтверждения.
Для получения токена отправьте запрос с вашим email и кодом подтверждения

```
POST   http://127.0.0.1:8000/api/v1/auth/token/
Content-Type: application/json

{
    "email": "g.o.borneo@yandex.ru",
    "confirmation_code": "<CONFIRMATION CODE>"
}
```
    **Запрос для получения списка произведений**
```
GET http://127.0.0.1:8000/api/v1/titles/
Content-Type: application/json
```

    **Оставить отзыв**
Оценка произведения производится по 10-ти бальной шкале.
```
POST   http://127.0.0.1:8000/api/v1/titles/1/reviews/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjAyNDk1MDY2LCJqdGkiOiI0MTk3NDdmYjllMDc0NDU4YmI3NzQwZmY3MTY0ZTE4ZSIsInVzZXJfaWQiOjF9.hfTeWcAC7PSwinEZS3R_J7vELtRUdoUfFqh8QjHhxJ0
Content-Type: application/json


{
    "text": "<REVIEW TEXT>",
    "score": <RATING>
}
```

