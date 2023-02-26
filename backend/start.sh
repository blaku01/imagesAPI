#!/bin/bash


python ./manage.py migrate
python -m gunicorn config.wsgi