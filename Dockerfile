FROM python:3.7-alpine
MAINTAINER Md Sazzad Ul Islam

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers musl-dev zlib zlib-dev

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app