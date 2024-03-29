{% set proj_slug = cookiecutter.project_slug %}
help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style"
	@echo "test - run tests quickly with the default Python"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "build - package"

all: default

default: clean dev_deps deps test lint build

.venv:
	if [ ! -e ".venv/bin/activate_this.py" ] ; then python3 -m venv .venv ; fi
	. .venv/bin/activate && pip install pip --upgrade

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr dist/

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

deps: .venv
	. .venv/bin/activate && pip install -U -r requirements.txt -t ./{{ proj_slug }}/libs

dev_deps: .venv
	. .venv/bin/activate && pip install -U -r requirements.txt
	. .venv/bin/activate && pip install -U -r dev_requirements.txt
	. .venv/bin/activate && pip install -U -r test_requirements.txt

lint:
	. .venv/bin/activate && flake8 {{ proj_slug }}/jobs {{ proj_slug }}/shared tests

test_no_spark:
	. .venv/bin/activate && PYTHONPATH=. pytest --cov-config=.coveragerc --cov={{ proj_slug }}/jobs --cov={{ proj_slug }}/shared --cov-report=html --junitxml=result.xml -s tests

test_with_spark:
	pip install -r requirements.txt
	pip install -r test_requirements.txt
	. .venv/bin/activate && PYTHONPATH=. pytest --cov-config=.coveragerc --cov={{ proj_slug }}/jobs --cov={{ proj_slug }}/shared --cov-report=html --junitxml=result.xml --withspark -s tests

build: clean deps
	mkdir ./dist
	cp ./{{ proj_slug }}/main.py ./dist
	zip -r dist/jobs.zip {{ proj_slug }}/__init__.py {{ proj_slug }}/jobs {{ proj_slug }}/shared
	cd ./{{ proj_slug }}/libs && zip -r ../../dist/libs.zip .

build_docs:
	. .venv/bin/activate && PYTHONPATH=. make -C docs html

start_spark_stack:
	docker stack deploy -c stack.yml {{ proj_slug }}
	docker stack ps {{ proj_slug }} --no-trunc

stop_spark_stack:
	docker stack rm {{ proj_slug }}

spark_stack_logs:
	docker logs $$(docker ps | grep jupyter | awk '{print $$1}')
