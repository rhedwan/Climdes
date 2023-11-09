
# Climdes API
## View Database Schema
- #### [Database Schema](https://dbdiagram.io/d/Climdes-Communities-64e6356202bd1c4a5e48f6ff)


# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone git@github.com/rhedwan/Climdes.git
    $ cd Climdes

Activate the virtualenv for your project.

Install project dependencies:

    $ pip install -r requirements.txt


Then simply apply the migrations:

    $ python manage.py migrate


You can now run the development server:

    $ python manage.py runserver
