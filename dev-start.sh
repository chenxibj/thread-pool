#!/bin/bash -e

BINDIR=$(dirname $0)

source $BINDIR/envfile

# start local mysql server
$BINDIR/start-local-mysql.sh

# start local rabbitmq server
$BINDIR/start-local-rabbitmq.sh

#apply django database migrations always, just in case this is not done
python $BINDIR/manage.py makemigrations
python $BINDIR/manage.py migrate

$BINDIR/start-project.sh
