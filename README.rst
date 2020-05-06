Album App for Flask
===================

ReportBro album application for Flask web framework. This is a fully working demo app to showcase
ReportBro and how you can integrate it in your Flask application.

The application is a simple web app and allows to manage a list of music albums.
ReportBro Designer is included so you can modify a template which is used
when you print a pdf of all your albums.

All Instructions in this file are for a Linux/Mac shell but the commands should
be easy to adapt for Windows.

Installation
------------

Clone git repository and change into repository dir:

.. code:: shell

    $ git clone https://github.com/jobsta/albumapp-flask.git
    $ cd albumapp-flask

Create virtual environment:

.. code:: shell

    $ python3 -m venv env

Activate virtual environment:

.. code:: shell

    $ . env/bin/activate

Install dependencies:

.. code:: shell

    $ python setup.py install

Configuration
-------------

- Create *.flaskenv* file to setup app, port (8000) and flask environment (development) by using *flaskenv_example* file:

.. code:: shell

    $ cp flaskenv_example .flaskenv

- Create and prepare the *instance* directory

.. code:: shell

    $ mkdir instance && mkdir instance/log

- Copy *config.py* into *instance/config.py*

.. code:: shell

    $ cp config.py instance

- Activate virtual environment (if not already active):

.. code:: shell

    $ . env/bin/activate

- Create database (creates albumapp.sqlite db in instance directory):

.. code:: shell

    $ flask db create

- Compile translation files so labels can be used in the application (generates messages.mo next to messages.po):

.. code:: shell

    $ flask translate compile

Run App
-------

Activate virtual environment (if not already active):

.. code:: shell

    $ . env/bin/activate

Start Flask webserver:

.. code:: shell

    $ flask run

Now your application is running and can be accessed here:
http://127.0.0.1:8000

IDE Configuration (PyCharm)
---------------------------

1. Open albumapp-flask repo directory

2. Add virtual env to project:

- Select File -> Settings
- Project: albumapp-flask -> Project interpreter
- click Settings-Icon and select "Add Local" option, select the recently created virtual env

3. Create new configuration: Edit Configurations...

4. Setup configuration:

- click + button and select Python
- Set name to something useful, e.g. *Debug*
- Python interpreter: select virtual env (if not already set)
- Script: select flask from virtual env (*env/bin/flask*)
- Script parameters: run
- Environment variables: ``FLASK_ENV=development``

Database
--------

An sqlite database is used to store application data (albums), report templates
and report previews used by ReportBro Designer.

To initially create the db with its tables:

Activate virtual environment:

.. code:: shell

    $ . env/bin/activate

Create database tables:

.. code:: shell

    $ flask db create


Translations
------------

Activate virtual environment:

.. code:: shell

    $ . env/bin/activate

Extract all texts to the .pot (portable object template) file and create translation file for given language locale:

.. code:: shell

    $ flask translate init

Update translation files:

.. code:: shell

    $ flask translate update

Compile translation files so labels can be used in the application (generates messages.mo next to messages.po):

.. code:: shell

    $ flask translate compile

Python Coding Style
-------------------

The `PEP 8 (Python Enhancement Proposal) <https://www.python.org/dev/peps/pep-0008/>`_
standard is used which is the de-facto code style guide for Python. An easy-to-read version
of PEP 8 can be found at https://pep8.org/
