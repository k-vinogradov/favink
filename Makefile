install:
	poetry install

check-code:
	poetry run black --check --diff favink tests/*
	poetry run pylint --disable=fixme  favink tests/*

test:
	poetry run pytest -vv

build:
	poetry build