FROM harborbj01.jcloud.com/library/django_pgabase:1.10
ADD . /export/App/project
ADD start-project.sh /export/App
