FROM ubuntu:14.04

ADD . /opt/yarr
WORKDIR /opt/yarr

RUN apt-get -y update
RUN apt-get -y install python python-pip python-dev mysql-server libmysqlclient-dev python-mysqldb
RUN service mysql start && mysql -u root -e "create database yarr"
RUN pip install -r requirements.txt
RUN service mysql start && (yes no | python manage.py syncdb) && python manage.py loaddata fixtures/initial.json

VOLUME /opt/yarr

EXPOSE 8000

CMD bash -l -c "cd /opt/yarr && service mysql start && python manage.py runserver 0.0.0.0:8000"

# docker build -t yarr .
# docker rm yarr; docker run -it -p 80:8000 -v `pwd`:/opt/yarr --name yarr yarr
# docker exec -it yarr bash -l
