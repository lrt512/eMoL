#!/bin/bash

pushd emol
pwd
poetry run gunicorn --access-logfile - --workers 1 --bind 0.0.0.0:8000 --reload emol.wsgi:application
popd