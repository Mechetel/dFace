FROM python:3.7

USER root

ENV PYTHONUNBUFFERED 1

RUN apt-get update -qq && apt-get install -y \
     nano

ENV APP_USER app

RUN useradd -m -d /home/$APP_USER $APP_USER
RUN mkdir /app && chown -R $APP_USER:$APP_USER /app

WORKDIR /app

RUN pip install Django psycopg2 django-environ

USER $APP_USER
