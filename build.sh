#!/usr/bin/env bash
# build.sh

python manage.py collectstatic --noinput
python manage.py migrate
