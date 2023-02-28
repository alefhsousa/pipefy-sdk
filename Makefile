build: build/install-dependencies

build/install-dependencies:
	poetry install

format:
	poetry run black .

test: test/static test/code

test/static: build
	poetry run black --check .
	# poetry run mypy --show-error-codes pipefy/

test/code:
	poetry run pytest -c pyproject.toml