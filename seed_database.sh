#!/bin/bash

rm db.sqlite3
rm -rf ./hunterapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations hunterapi
python3 manage.py migrate hunterapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

