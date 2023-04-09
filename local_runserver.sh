#!/bin/bash

source .venv/bin/activate
pushd emol
./manage.py runserver
popd