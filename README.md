Installation
============

First, set up MySQL and Python+PIP. The default setup uses the mysql
user `root` with an empty password and the database is named `yarr`Then:

    $ pip install -r requirements.txt


Loading Initial Data
====================

    $ ./manage.py migrate
    $ ./manage.py loaddata fixtures/initial.json


Starting
========

    $ ./manage.py runserver
