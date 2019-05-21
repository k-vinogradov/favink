install:
	poetry install

check-code:
	poetry run black --check --diff favink tests/*
	poetry run pylint --disable=fixme,missing-docstring  favink tests/*

test:
	poetry run pytest -vv

build: check-code test
	poetry build