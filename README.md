Installation
============

First, set up MySQL, Python+PIP and [Bower](http://bower.io/). Then:

    $ pip install -r requirements.txt
    $ cd frontend && bower install


Loading Initial Data
====================

    $ ./manage.py migrate
    $ ./manage.py loaddata fixtures/initial.json


Starting
========

    $ ./manage.py runserver
