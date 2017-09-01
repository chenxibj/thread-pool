#!/bin/bash

BINDIR=$(dirname $0)
source $BINDIR/envfile
MYSQL_IMAGE="harborbj01.jcloud.com/iaas/mysql:5.6.37"
RUN_MYSQL_CMD="docker run --net=host --rm $MYSQL_IMAGE"
MYSQL_OPTS=" -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USER -p$MYSQL_PASS"


echo "check if mysql is already running"
$RUN_MYSQL_CMD mysqladmin $MYSQL_OPTS status >& /dev/null
if [ $? -eq 0 ]; then
  echo "mysql is already running, skipping"
  exit 0
fi

docker run -p $MYSQL_PORT:3306 -d -e MYSQL_ROOT_PASSWORD=$MYSQL_PASS -e MYSQL_ROOT_HOST=% $MYSQL_IMAGE

#wait for database to be up and running
$BINDIR/check-mysql.sh

echo "Create ads database ..."
$RUN_MYSQL_CMD mysql $MYSQL_OPTS -e "create database ads"
if [ $? -ne 0 ]; then
  echo "Failed to create database ads"
  exit 1
else
  echo "Database ads is created successfully"
fi
