#!/bin/bash

GREEN='\033[1;32m'
RESET='\033[0m'

echo -e "${GREEN}Database configuration${RESET}"

cd /opt/emol
echo "Apply migrations"
/opt/venv/bin/python manage.py migrate

echo "Collect static files"
/opt/venv/bin/python manage.py collectstatic --noinput

echo "Create cache table if needed"
/opt/venv/bin/python manage.py createcachetable

echo "Create superuser if needed"
/opt/venv/bin/python manage.py ensure_superuser
