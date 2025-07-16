.PHONY: all test pytest lint ruff clean

all: lint test

test:
	pytest

lint:
	ruff format
	ruff check --fix

ruff: lint

clean:
	rm output/*.md