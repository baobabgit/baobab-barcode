# Validation qualité (Unix / Git Bash / WSL). Nécessite Python et les extras [dev].

.PHONY: quality clean-coverage
quality:
	python -m black --check src tests
	python -m flake8 src tests
	python -m pylint src tests
	python -m mypy
	python -m bandit -c pyproject.toml -q -r src
	python -m pytest

clean-coverage:
	rm -rf docs/tests/coverage/html
	rm -f docs/tests/coverage/coverage.xml docs/tests/coverage/.coverage docs/tests/coverage/.coverage.*
