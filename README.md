# Phone calls time tracker

## Abstract
This is a simple api created to Olist company as they ask as part of they hiring process.
It's made with python and it doesn't really use the most bleeding edge stack out there. Some simplicity was required to keep the code understandable, however, i have learned something about the libs i have chosen and discovered new and better ones when everything was almost ready. I intend to improve this overtime

## Stack
* Python 3.6
* Flask + Flask-RestPlus
* SQLAlchemy
* Alembic
* setuptools
* OpenApi spec

## Philosophy
Although python's philosofy is to not raise too much walls around the code, i'm inclined to use OOP in other to bring cohesion to the code and define the exact responsability of each element and so they have to be valid enough to be composed one to another.

I'm also very inclined to use DDD techniques, and i was intending to use the 
SQLAlchemy's classical mappings, however i've stumbled on some problems with this approach and for the time being i'm falling back to declarative style.

All of this part of my personal taste however. I am always open to use any other coding styles. I strongly believe that each company has to find its principles and everyone has to work aligned to those principles, so whatever is the Olist aproach i will gladly follow

## Running the project
Start a python virtualenv or the docker container using the docker-compose command.
if you are using the virtualenv you need to install the dependencies and start up the server:
```
$ python setup.py install
$ pipenv install
$ python app.py
```

Run the migrations:
```
$ alembic upgrade head
```
Note: the project itself is configured to run on mysql, that can be changed on the infrastructure/repository.py

### Docker
It's also possible to run this app on a docker container wich is configured using docker-compose. It will run on development mode
```
# docker-compose up -d
```
after instalation, run migrations:
```
# docker-compose exec python alembic upgrade head
```

## Controversial design decisions
I have decided to not use the type field because it seemed more performatic to use only one table for the two endpoints,
besides the fact that having two diferent endpoints was enough for the app know what was being posted, and made it easier
to achieve single responsability by eliminating the need to use ifs to distinguish the api payload

## Database design
Indexes has been used on the date fields and also on the source and destination ones, in order to make the needed queries
faster and less resourcefull.

Alembic was used to carry on migrations. Its a great tool created by the very same guy who created sqlalchemy, needlesly
to say that it is fully compatible with sqlalchemy

## Api documentation
When you get the project running, open it on the browser on the root path, a swagger-ui will be presented as the documentation

## Running tests
Simply run unittest
```
$ pyhton -m unittest test.py
```
