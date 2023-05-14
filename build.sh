#!/bin/bash

## install requirements
source .venv/bin/activate
pip install -r requirements.txt

## collect static files
python3 manage.py collectstatic --noinput

## apply migrations
python3 manage.py migrate
