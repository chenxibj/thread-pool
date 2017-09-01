#!/bin/bash

BINDIR=$(dirname $0)

#source required environment variable
#not exporting in environment file due to format issue with docker --env-file option 
source $BINDIR/envfile

#check if mysql is up and running
TIMEOUT=60
count=0
while(true); do
  if mysqladmin -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASS -P$MYSQL_PORT status >& /dev/null; then
    break;
  else
    count=$(expr $count + 1)
    echo "Waiting 1 second for database to be up and running..."
    sleep 1;
  fi
  if [ $count -gt $TIMEOUT ]; then
    echo "ERROR: mysql check timeout after $TIMEOUT seconds"
    exit 1
  fi
done
