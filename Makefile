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
	pip install requirements.txt
	pip install -e .

token:
	python examples/example_get_labels.py

requirements:
	pip freeze > requirements.txt

clean:
	rm output/*.md

generate_summary_collection:
	python scripts/generate_summary_collection.py

delete_last_markdown_edition:
	python scripts/delete_last_markdown_edition.py

regenerate_last_markdown_edition: delete_last_markdown_edition generate_summary_collection
