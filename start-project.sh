#!/bin/bash

BINDIR=$(dirname $0)
#check whether required environment variables are set properly
#for varname in JNS_URL LORD_URL LORD_TOKENS_JSON MYSQL_HOST MYSQL_PORT MYSQL_USER MYSQL_PASS
#do
  #if [ -z "${!varname}" ]; then
    #echo "ERROR: environment variable $varname is required setting, abort!"
    #exit 1
  #fi
#done

#apply django database migrations always, just in case this is not done
#python $BINDIR/manage.py makemigrations
#python $BINDIR/manage.py migrate
python $BINDIR/project/manage.py runserver 0.0.0.0:8080
