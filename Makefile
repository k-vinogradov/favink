install:
	poetry install

check-code:
	poetry run black --check --diff favink
	poetry run pylint favink

test:
	poetry run pytest -v

build:
	poetry build