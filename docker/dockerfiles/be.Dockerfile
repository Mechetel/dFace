FROM python:3.9

USER root

ENV PYTHONUNBUFFERED 1

RUN apt-get update -qq && apt-get install -y \
      nano\
      net-tools\
      bzip2 \
      g++ \
      git \
      graphviz \
      libgl1-mesa-glx \
      libhdf5-dev \
      openmpi-bin \
      wget \
      python3-tk && \
    rm -rf /var/lib/apt/lists/*

ENV APP_USER app

RUN useradd -m -d /home/$APP_USER $APP_USER
RUN mkdir /app
COPY requirements.txt app/requirements.txt
RUN chown -R $APP_USER:$APP_USER /app

WORKDIR /app

# Minimize image size
RUN (apt-get autoremove -y; apt-get autoclean -y)
ENV QT_X11_NO_MITSHM=1

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

USER $APP_USER
