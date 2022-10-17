
all: build run

build:
	docker compose build

run:
	docker compose up -d

run-shell:
	docker compose up

down:
	docker compose down

down-volume:
	docker compose down -v

web:
	docker compose run --rm --service-ports web

shell:
	docker compose run --rm --entrypoint=flask web shell

run-tests:
	docker compose run --rm --entrypoint=pytest web -v

isort:
	docker compose run --rm --no-deps --entrypoint=isort web .

flake:
	docker compose run --rm --no-deps --entrypoint=flake8 web .

setup:
	pip install -r requirements/common.txt