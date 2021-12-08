FROM python:3.7

USER root

ENV PYTHONUNBUFFERED 1

RUN apt-get update -qq && apt-get install -y \
     nano

ENV APP_USER app

RUN useradd -m -d /home/$APP_USER $APP_USER
RUN mkdir /app && chown -R $APP_USER:$APP_USER /app

WORKDIR /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install Django psycopg2 django-environ

USER $APP_USER
