FROM python:3.9

USER root

ENV PYTHONUNBUFFERED 1
ENV QT_X11_NO_MITSHM 1

RUN apt-get update -qq && apt-get install -y \
      nano\
      python3-opencv

ENV APP_USER app

RUN useradd -m -d /home/$APP_USER $APP_USER
RUN mkdir /app
RUN chown -R $APP_USER:$APP_USER /app

WORKDIR /app

# Minimize image size
RUN (apt-get autoremove -y; apt-get autoclean -y)

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install Django \
                 django-environ \
                 # keras \
                 # numpy \
                 # facenet-pytorch \
                 neovim \
                 opencv-python \
                 pynvim \
                 psycopg2 \
                 pydantic \
                 fontawesomefree \
                 hikload


USER $APP_USER
