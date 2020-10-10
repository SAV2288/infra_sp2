FROM python:3.8.5
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000 # Без данной строки не проходят тесты при загрузке на проверку. Если оставлять команды в этом файле или выносить в docker-compose только команду применения миграций, то миграции не проходят. Так же загрузил в гит файл .env т.к. без него не проходят тесты
