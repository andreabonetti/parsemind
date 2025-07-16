.PHONY: all test pytest lint ruff clean requirements

all: lint test freeze

test:
	pytest

lint:
	ruff format
	ruff check --fix

ruff: lint

requirements:
	pipreqs . --force

clean:
	rm output/*.md