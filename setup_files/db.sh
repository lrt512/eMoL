#!/bin/bash

GREEN='\033[1;32m'
RESET='\033[0m'

echo -e "${GREEN}Database configuration${RESET}"

cd /opt/emol/emol
echo "Apply migrations"
poetry run python manage.py migrate

echo "Collect static files"
poetry run python manage.py collectstatic --noinput

echo "Create cache table if needed"
poetry run python manage.py createcachetable

echo "Create superuser if needed"
poetry run python manage.py ensure_superuser
