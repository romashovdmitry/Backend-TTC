FROM python:3.12-bullseye as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./Docker/Django/requirements.txt /app
COPY ./app /app

RUN pip install --no-cache-dir -r requirements.txt ; \
    pip install --no-cache-dir gunicorn ; \
    pip install --no-cache-dir aiogram ; \
    pip install --no-cache-dir uvicorn[standard] ; \
    pip install --no-cache-dir channels_redis

EXPOSE 8000

# HEALTHCHECK CMD curl -sS http://localhost:8000 || exit 1

LABEL description="Install packages and run Django project"

FROM base as wsgi
CMD sh -c "python manage.py makemigrations && python manage.py migrate && python manage.py create_admin && python manage.py runserver 0.0.0.0:8001"

FROM base as asgi
CMD ["gunicorn", "main.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8002", "--reload"]
