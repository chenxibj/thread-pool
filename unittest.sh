#!/bin/bash

BINDIR=$(dirname $0)

#source required environment variable
#not exporting in environment file due to format issue with docker --env-file option
source envfile

python manage.py makemigrations
python manage.py migrate
python manage.py test
