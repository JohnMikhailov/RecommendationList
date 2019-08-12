FROM python:3.6.9-alpine3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk add --no-cache postgresql-libs

RUN python3 -m pip install pipenv

COPY Pipfile Pipfile.lock /app/

RUN \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 apk add --no-cache jpeg-dev zlib-dev && \
 apk add --no-cache libmemcached-dev && \
 python3 -m pipenv install --system --skip-lock && \
 apk --purge del .build-deps

COPY . /app/
EXPOSE 8000

ENTRYPOINT ["/bin/sh", "./docker-entrypoint.sh"]
