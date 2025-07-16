.PHONY: all test pytest lint ruff clean requirements

all: lint test requirements

test:
	pytest

lint:
	ruff format
	ruff check --fix

ruff: lint

requirements:
	pip freeze > requirements.txt

clean:
	rm output/*.md