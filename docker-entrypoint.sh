#!/bin/sh
python3 TopList/manage.py migrate
python3 TopList/manage.py runserver 0.0.0.0:8000
#! python TopList/manage.py collectstatic
#! gunicorn TopList.TopList.wsgi:application -w 3 -b 0.0.0.0:${PORT:-8000}