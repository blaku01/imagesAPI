#!/bin/bash

python ./manage.py collectstatic --no-input
python ./manage.py migrate
python -m gunicorn config.wsgi