SHELL := /bin/bash
VIRTUALENV_ROOT := $(shell [ -z $$VIRTUAL_ENV ] && echo $$(pwd)/venv || echo $$VIRTUAL_ENV)

virtualenv:
	[ -z $$VIRTUAL_ENV ] && [ ! -d venv ] && virtualenv venv || true

requirements: virtualenv
	${VIRTUALENV_ROOT}/bin/pip install -r pages_builder/requirements.txt

requirements_for_test: virtualenv
	${VIRTUALENV_ROOT}/bin/pip install -r pages_builder/requirements_for_test.txt

generate_pages: requirements
	${VIRTUALENV_ROOT}/bin/python pages_builder/generate_pages.py

serve_pages: generate_pages
	cd pages && ${VIRTUALENV_ROOT}/bin/python -m SimpleHTTPServer

watch_for_changes: generate_pages
	${VIRTUALENV_ROOT}/bin/python pages_builder/watch_for_changes.py

test: test_pep8 test_python

test_pep8:
	${VIRTUALENV_ROOT}/bin/pep8 ./pages_builder_2

test_python:
	${VIRTUALENV_ROOT}/bin/py.test ${PYTEST_ARGS}
