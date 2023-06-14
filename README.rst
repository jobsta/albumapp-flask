Album App for Flask
===================

ReportBro album application for Flask web framework. This is a fully working demo app to showcase
ReportBro and how you can integrate it in your Flask application.

The application is a simple web app and allows to manage a list of music albums.
ReportBro Designer is included so you can modify a template which is used
when you print a pdf of all your albums.

The Demo App is also avaiable for the `Django <https://www.djangoproject.com/>`_
and `web2py <http://web2py.com/>`_ web frameworks. See
`Album App for Django <https://github.com/jobsta/albumapp-django.git>`_ and
`Album App for web2py <https://github.com/jobsta/albumapp-web2py.git>`_ respectively.

All Instructions in this file are for a Linux/Mac shell but the commands are
easy to adapt for Windows. If a command is different for Windows then
it will be shown below. Commands which can be done in
Windows Explorer (e.g. copy file, create directory) are not explicitly listed
for Windows.


Installation
------------

Clone the git repository and change into the created directory:

.. code:: shell

    $ git clone https://github.com/jobsta/albumapp-flask.git
    $ cd albumapp-flask

This app requires poetry (version 1.2.2 or newer) to be installed and working. See https://python-poetry.org/docs/#installation
for installation details.

Install all dependencies:

.. code:: shell
    $ poetry install

To activate the virtual environment:

.. code:: shell

    $ poetry shell

Configuration
-------------

- Create a *.flaskenv* file to setup app, port (5000) and the flask environment (set to development in the example)
by copying the file *flaskenv_example*:

.. code:: shell

    $ cp flaskenv_example .flaskenv

- Create and prepare the *instance* directory

.. code:: shell

    $ mkdir instance && mkdir instance/log

- Copy the example configuration *config.py* into *instance/config.py*

.. code:: shell

    $ cp config.py instance

- Create a database (creates albumapp.sqlite in the instance directory):

.. code:: shell

    $ poetry run flask db create

- Compile all translation files so the labels can be used in the application
(generates messages.mo next to messages.po):

.. code:: shell

    $ poetry run flask translate compile

Run App
-------

Start the Flask webserver:

.. code:: shell

    $ poetry run flask run

Now your application is running and can be accessed here:
http://127.0.0.1:5000

IDE Configuration (PyCharm)
---------------------------

1. Open the cloned albumapp-flask directory

2. Add virtual env to project:

- Select File -> Settings
- Project: albumapp-flask -> Project interpreter
- click Settings-Icon and select "Add Local" option
- Choose "Poetry Environment" and select "Existing Environment"

3. Create a new configuration: Edit Configurations...

4. Setup configuration:

- click + button and select Python
- Set the name to something useful, e.g. *Debug*
- Python interpreter: select virtual env (if not already set)
- Script: select flask from virtual env (*env/bin/flask*)
- Script parameters: run
- Environment variables: ``FLASK_ENV=development``

Database
--------

sqlite is used as database to store the application data (albums),
report templates and report previews used by ReportBro Designer.

To initially create the db with its tables the following steps are necessary:

Create database (creates albumapp.sqlite db in the instance directory):

.. code:: shell

    $ poetry run flask db create


Translations
------------

Extract all texts to the .pot (portable object template) file and create translation file for a given language locale:

.. code:: shell

    $ poetry run flask translate init

Update the translation files:

.. code:: shell

    $ poetry run flask translate update

Compile the translation files that the labels can be used in the application
(generates messages.mo next to messages.po):

.. code:: shell

    $ poetry run flask translate compile

Python Coding Style
-------------------

The `PEP 8 (Python Enhancement Proposal) <https://www.python.org/dev/peps/pep-0008/>`_
standard is used which is the de-facto code style guide for Python. An easy-to-read version
of PEP 8 can be found at https://pep8.org/
