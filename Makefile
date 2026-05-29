.PHONY: install test

install:
	poetry install --no-interaction --no-ansi

test:
	pytest
