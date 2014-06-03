     Instantly Shared Hospital Records
========================

Welcome to the Menu Orders application

Below you will find basic setup instructions for the ``Instantly Shared Hospital Records``
project. To begin you should have the following applications installed on your
local development system:

- `Python >= 2.6 (2.7 recommended) <http://www.python.org/getit/>`_
- `pip >= 1.1 <http://www.pip-installer.org/>`_
- `virtualenv >= 1.8 <http://www.virtualenv.org/>`_

Getting Started
---------------

To setup your local environment you should create a virtualenv and install the
necessary requirements::

    virtualenv --distribute shared_hospital_records-env

On Posix systems you can activate your environment like this::

    source shared_hospital_records-env/bin/activate

On Windows, you'd use::

    shared_hospital_records-env\Scripts\activate

Then::

    cd shared_hospital_records

Run syncdb::

    ./manage.py syncdb
    ./manage.py migrate

You should now be able to run the development server::

    ./manage.py runserver


