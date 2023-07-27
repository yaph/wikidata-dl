.PHONY: build clean release

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -f .coverage
	rm -fr .pytest_cache
	rm -fr htmlcov/
	rm -f dist/*



coverage:
	pytest --cov-report=term-missing --cov-config=pyproject.toml --cov=wikidata_dl --cov=tests


checks:
	flake8 wikidata_dl tests
	mypy -p wikidata_dl
	pytest -s


# Build source and wheel packages
build: clean checks
	hatch build


test-cli:
	rm -rf tests/data/
	wikidata_dl/cli.py --cache-dir tests/data --format json tests/queries/continents-on-earth.sparql
	wikidata_dl/cli.py --cache-dir tests/data --items tests/queries/continents-on-earth.sparql
	wikidata_dl/cli.py --cache-dir tests/data --timeout 0 tests/queries/nevada-events.sparql


# Call example: make release version=2023.07.27
release: build
	git tag -a $(version) -m 'Create version $(version)'
	git push --tags
	hatch publish
