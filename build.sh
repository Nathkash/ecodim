#!/usr/bin/env bash
set -e

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py init_classes
python manage.py create_president