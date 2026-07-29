#!/bin/bash
#by claude.ai
set -e  # stop if any command fails

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
