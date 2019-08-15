#!/bin/sh
while ! nc -z postgres 5432;
do
    sleep 0.1;
done;
python3 TopList/manage.py migrate
python3 TopList/manage.py runserver 0.0.0.0:8000
#! python TopList/manage.py collectstatic
#! gunicorn config.wsgi:application -w 3 -b 0.0.0.0:${PORT:-8000}