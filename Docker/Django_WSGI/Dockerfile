FROM python:3.12-bullseye as Python

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./Docker/Django_WSGI/requirements.txt /app
COPY ./app /app

RUN pip install -r requirements.txt

EXPOSE 8000

# HEALTHCHECK CMD curl -sS http://localhost:8000 || exit 1

LABEL description="Install packages and run Django project"