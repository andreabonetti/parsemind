.PHONY: all test pytest lint ruff clean requirements token

# ----- all -----

all: lint test requirements

# ----- test -----

pytest:
	pytest

test: pytest

# ----- lint -----

ruff:
	ruff format
	ruff check --fix

mypy:
	mypy .

lint: ruff mypy

# ----- misc -----

install:
	pip install --upgrade pip
	pip install -e .

token:
	python examples/example_get_labels.py

requirements:
	pip freeze > requirements.txt

clean:
	rm output/*.md