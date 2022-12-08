.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . \( -path ./env -o -path ./venv -o -path ./.env -o -path ./.venv \) -prune -o -name '*.egg-info' -exec rm -fr {} +
	find . \( -path ./env -o -path ./venv -o -path ./.env -o -path ./.venv \) -prune -o -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

format: ## check style with flake8
	isort core_service_lib
	isort tests
	black core_service_lib
	black tests

lint: ## check style with flake8
	flake8 --exit-zero core_service_lib tests
	pylint --rcfile=tests/.pylintrc tests/** ; pylint-exit --error-fail $$?
	pylint core_service_lib/** ; pylint-exit --error-fail $$?

test: ## run tests quickly with the default Python
	py.test

test-cov:  ## test and generate converage
	#pytest --cov=src --junitxml=build/reports/tests.xml --cov-report term-missing --cov-report xml:build/reports/cobertura-coverage.xml --cov-report html:build/reports/cobertura-coverage
	pytest --junit-xml build/reports/tests.xml --cov=core_service_lib --cov-report term-missing --cov-report html:build/reports/coverage-reports/html-coverage --cov-report xml:build/reports/coverage-reports/coverage.xml

merge-reports: ## Merge report
	find reports/ -mindepth 1 -maxdepth 1 -type d | xargs rm -rf
	cp -rf docs/build/html reports/.
	cp -rf build/reports/coverage-reports/html-coverage reports/.

coverage: ## check code coverage quickly with the default Python
	coverage run --source core_service_lib -m pytest
	coverage report -m
	coverage html -d build/reports/coverage-reports/html-coverage
	$(BROWSER) build/reports/coverage-reports/html-coverage/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/source/core_service_lib.rst
	rm -f docs/source/modules.rst
	sphinx-apidoc -o docs/source/generated core_service_lib
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

servedocs: docs ## compile the docs watching for changes
	$(BROWSER) docs/_build/html/index.html

release: dist ## package and upload a release
	# call poetry instead
	#twine upload dist/*

executable:
	pyinstaller --name core_service_lib core_service_lib/service.py

dist: clean docs ## builds source and wheel package
	poetry build
	ls -l dist

notice:
	poetry export -f requirements.txt --output requirements.txt
	sed -i "s/-e .//g" requirements.txt
	liccheck -s licenses_strategy.ini
	pip-licenses --from=mixed > NOTICE
	rm requirements.txt

watchc:
	ptw --runner "pytest -m current" --ext ".py,.feature,.yml,.yaml,.html"

watcha:
	ptw --runner "pytest --cov-report term-missing:skip-covered --cov=core_service_lib" --ext ".py,.feature,.yml,.yaml,.html" --onpass "make lint"
