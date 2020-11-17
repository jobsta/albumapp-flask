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

Create a virtual environment called env:

.. code:: shell

    $ python3 -m venv env

Activate the virtual environment:

.. code:: shell

    $ . env/bin/activate

On Windows the virtual environment is activated this way instead:

.. code:: shell

    $ env\Scripts\activate

Once the virtual environment is activated you should see the environment name prepended to the shell prompt.

Install all required dependencies:

.. code:: shell

    $ python setup.py install

Configuration
-------------

- Create a *.flaskenv* file to setup app, port (8000) and the flask environment (set to development in the example)
by copying the file *flaskenv_example*:

.. code:: shell

    $ cp flaskenv_example .flaskenv

- Create and prepare the *instance* directory

.. code:: shell

    $ mkdir instance && mkdir instance/log

- Copy the example configuration *config.py* into *instance/config.py*

.. code:: shell

    $ cp config.py instance

- Activate the virtual environment (if not already active):

.. code:: shell

    $ . env/bin/activate

- Create a database (creates albumapp.sqlite in the instance directory):

.. code:: shell

    $ flask db create

- Compile all translation files so the labels can be used in the application
(generates messages.mo next to messages.po):

.. code:: shell

    $ flask translate compile

Run App
-------

Activate the virtual environment (if not already active):

.. code:: shell

    $ . env/bin/activate

Start the Flask webserver:

.. code:: shell

    $ flask run

Now your application is running and can be accessed here:
http://127.0.0.1:8000

IDE Configuration (PyCharm)
---------------------------

1. Open the cloned albumapp-flask directory

2. Add virtual env to project:

- Select File -> Settings
- Project: albumapp-flask -> Project interpreter
- click Settings-Icon and select "Add Local" option, select the recently created virtual env

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

Activate the virtual environment:

.. code:: shell

    $ . env/bin/activate

Create database (creates albumapp.sqlite db in the instance directory):

.. code:: shell

    $ flask db create


Translations
------------

Activate the virtual environment:

.. code:: shell

    $ . env/bin/activate

Extract all texts to the .pot (portable object template) file and create translation file for a given language locale:

.. code:: shell

    $ flask translate init

Update the translation files:

.. code:: shell

    $ flask translate update

Compile the translation files that the labels can be used in the application
(generates messages.mo next to messages.po):

.. code:: shell

    $ flask translate compile

Python Coding Style
-------------------

The `PEP 8 (Python Enhancement Proposal) <https://www.python.org/dev/peps/pep-0008/>`_
standard is used which is the de-facto code style guide for Python. An easy-to-read version
of PEP 8 can be found at https://pep8.org/
