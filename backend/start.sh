#!/bin/bash


python ./generate_fixtures.py
python ./manage.py runserver 0.0.0.0:8000