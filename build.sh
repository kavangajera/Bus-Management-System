#!/usr/bin/env bash
# build.sh

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
