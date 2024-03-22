# django-hydroponics
This is the implementation of a simple hydroponics management system with CRUD operations on system, JWT Authentication and an ability to add water measurements to any user's system.

## Applied Technologies
- Django (+ Rest Framework + drf for documentation)
- Docker
- PostgreSQL

## Use Cases
- CRUD operations on hydroponic systems (+ PATCH)
- Provide measurements for user's owned systems
- Detail specified system with including 10 last measurements

## Documentation
Generated documentation (OpenAPI 3 format) can be found in `docs`.

Swagger documentation works on http://localhost:8000/doc/swagger/

## How To Run
1. Create your own `.env` file based on `.sample.env`.
1. In the root of the project, type `docker-compose build`.
1. Type `docker-compose up`. After that, API should run on 8000 port.
1. Type `docker exec -it hydroponics_django bash` to open a container's
command line.
1. Apply migrations by `python manage.py makemigrations` followed by
`python manage.py migrate`.
1. After that, everything should work.