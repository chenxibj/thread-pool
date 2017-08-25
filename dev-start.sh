#!/bin/bash -e

BINDIR=$(dirname $0)

source $BINDIR/envfile

# start local mysql server
$BINDIR/start-local-mysql.sh

# start local rabbitmq server
$BINDIR/start-local-rabbitmq.sh

$BINDIR/start-project.sh
