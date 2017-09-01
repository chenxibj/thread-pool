#!/bin/bash

BINDIR=$(dirname $0)
#check whether required environment variables are set properly
for varname in MYSQL_HOST MYSQL_PORT MYSQL_USER MYSQL_PASS
do
  if [ -z "${!varname}" ]; then
    echo "ERROR: environment variable $varname is required setting, abort!"
    exit 1
  fi
done

python $BINDIR/conv.py
nohup python $BINDIR/node_deploy/deploy_worker.py > test.log 2>&1 &
python $BINDIR/manage.py makemigrations
python $BINDIR/manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'caoronglu@jd.com', 'Jcl0ud#');" | python $BINDIR/manage.py shell
python $BINDIR/manage.py runserver 0.0.0.0:8080
