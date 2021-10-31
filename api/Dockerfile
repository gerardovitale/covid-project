FROM python:3.8-alpine AS compile-image

RUN apk update &&\
    apk add --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /requirements.txt


FROM python:3.8-alpine AS build-image

MAINTAINER Gerardo Vitale
LABEL name="PySparkApp" \
      license="MIT License"

COPY --from=compile-image /opt/venv /opt/venv

ENV PATH=/opt/venv/bin:$PATH \
    PYTHONPATH=/opt/venv/bin:$PYTHONPATH \
    PYTHONUNBUFFERED=1

COPY . /api/

ENTRYPOINT ["python", "-u", "run.py"]
