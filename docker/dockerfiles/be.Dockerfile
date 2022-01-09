FROM python:3.7

USER root

ENV PYTHONUNBUFFERED 1

RUN apt-get update -qq && apt-get install -y \
     nano net-tools

ENV APP_USER app

RUN useradd -m -d /home/$APP_USER $APP_USER
RUN mkdir /app && chown -R $APP_USER:$APP_USER /app

WORKDIR /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install Django psycopg2 django-environ

USER $APP_USER

# RUN arp -an | grep -E 'bc:ba:c2:44:a3:4f' | awk '{print $2}' | sed 's/^.//;s/.$//' > docker/secret-envs/cameras_ip.env
