#!/bin/bash

BINDIR=$(dirname $0)
source $BINDIR/envfile
RABBITMQ_IMAGE="harborbj01.jcloud.com/iaas/rabbitmq:3.6.11"
docker run -d -p 5672:5672 --rm $RABBITMQ_IMAGE

#wait for database to be up and running
#todo: add rabbitmq startup check
sleep 5
