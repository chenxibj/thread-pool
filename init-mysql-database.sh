#!/bin/bash

BINDIR=$(dirname $0)
source $BINDIR/envfile
MYSQL_OPTS=" -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USER -p$MYSQL_PASS"

#check if mysql is up and running
TIMEOUT=60
count=0
while(true); do
  if mysqladmin $MYSQL_OPTS status >& /dev/null; then
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

#check if ads db exists
if mysql $MYSQL_OPTS -e "show databases" | grep ads; then
  echo "Warning: database ads already exists, skip creating again"
  exit 0
fi
echo "Create ads database ..."
mysql $MYSQL_OPTS -e "create database ads"
if [ $? -ne 0 ]; then
  echo "Failed to create database ads"
  exit 1
else
  echo "Database ads is created successfully"
fi
