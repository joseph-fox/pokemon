.PHONY: all

## Provision and spin up the development containers
build-dev-image:
	docker-compose build && docker-compose up -d --scale web=0

## Database migration.
db-migrate:
	docker-compose run --rm web ./manage.py migrate

## Reset database.
db-reset:
	docker-compose run --rm web ./manage.py reset_db

## Start development server.
start-service:
	docker-compose run --rm --service-ports web ./manage.py runserver 0.0.0.0:5090 --settings=pokemon.config.dev

## Kill containers
halt:
	docker-compose down

## Automatically generate migrations
db-makemigrations:
	docker-compose run --rm web ./manage.py makemigrations

## Start shell inside the container
start-shell:
	docker-compose run --rm --service-ports web bash

## Run test
run-test:
	docker-compose run --rm --service-ports web pytest --cache-clear --create-db --cov=pokemon


