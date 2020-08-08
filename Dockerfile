FROM python:3.7-alpine
MAINTAINER Md Sazzad Ul Islam

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1 #Prevents Python from writing pyc files to disc
ENV PYTHONUNBUFFERED 1 #Prevents Python from buffering stdout and stderr
ENV DEBUG 0

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers musl-dev zlib zlib-dev

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

CMD gunicorn app.wsgi:application --bind 0.0.0.0:$PORT