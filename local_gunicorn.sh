#!/bin/bash

pushd emol
pwd
../.venv/bin/gunicorn --access-logfile - --workers 1 --bind 0.0.0.0:8000 --reload emol.wsgi:application
popd