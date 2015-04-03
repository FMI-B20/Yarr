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


Login API
=========

Registration.
POST data to:

'http://localhost:8000/rest-auth/registration/' with payload
{"username": "dragos2", "password1": "dragos2", "password2": "dragos2",
"email": "dragos2@mail.com"}

Login.
POST data to:

'http://localhost:8000/rest-auth/login/' {"username": "dragos2", "password": "dragos2"}

More details about the
[API](http://django-rest-auth.readthedocs.org/en/latest/api_endpoints.html)
