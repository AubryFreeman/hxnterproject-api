#!/bin/bash

rm db.sqlite3
rm -rf ./hxnterapiapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations hxnterapiapi
python3 manage.py migrate hxnterapiapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata hunter
# python3 manage.py loaddata mission
python3 manage.py loaddata wanted
python3 manage.py loaddata type

