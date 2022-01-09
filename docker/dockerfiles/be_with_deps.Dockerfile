FROM python:3.7

USER root

ENV PYTHONUNBUFFERED 1

RUN apt-get update -qq && apt-get install -y \
     nano net-tools

WORKDIR /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . /app
