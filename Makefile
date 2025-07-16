.PHONY: all test pytest lint ruff clean requirements

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

requirements:
	pip freeze > requirements.txt

clean:
	rm output/*.md