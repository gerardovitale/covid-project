FROM python:3.8-alpine
# MAINTAINER Gerardo Vitale

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk update
RUN apk update \
    && apk add --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers
RUN pip install --upgrade pip && \
    pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /api
WORKDIR /api
COPY . /api/

RUN adduser -D user
USER user