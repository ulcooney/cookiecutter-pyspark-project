===============================
{{ cookiecutter.project_name }}
===============================
{% set proj_slug = cookiecutter.project_slug %}

Setting up a local development environment
==========================================

To install all development dependencies in a local virtual environment run the
following::

    make dev_deps

Running test suite
==================

To run the test suite::

    make test

Build documentation
===================

To build sphinx documentation::

    make build_docs

The html documentation can be found at *./docs/_build/html*. For local use
open *index.html* in your browser.

Build deployable artifacts
==========================

To build the artifacts that can be submitted and executed in a Spark environment::

    make build

The artifacts can be found at *./dist*

Start Spark / Jupyter Notebook stack 
====================================
The docker stack provides a containerised spark and jupyter notebook environment
that you can use for local development and testing.

The stack requires an up-to-date installation of docker
(see `Setting up Docker`_).

To start the stack::

    make start_spark_stack

To view the logs from the jupyter stack::

    make spark_stack_logs

This can be particularly useful to find the url and token for the jupyter
notebook web interface.

To stop the stack::

    make stop_spark_stack

To submit a job to the Spark container you should first build the project (
see `Build deployable artifacts`_). Then open the jupyter notebook
home page and launch a new terminal::

    cd dist
    /usr/local/spark/bin/spark-submit --py-files jobs.zip,libs.zip main.py --job <job_name>
    # eg to submit the word count demo job.
    /usr/local/spark/bin/spark-submit --py-files jobs.zip,libs.zip main.py --job word_count_demo


Where *<job_name>* is the name of the module in the *jobs* directory eg *word_count_demo*.

Setting up Docker
=================

Follow the `installation instructions for Docker-CE`_ for your OS.

Initialise Docker Swarm::

    docker swarm init

If you have multiple IP addresses you will have to specify a specific address eg::

    docker swarm init --advertise-addr 10.169.98.38

.. _`installation instructions for Docker-CE`: https://docs.docker.com/install/

Creating new jobs
=================

Create a new module with a meaningful name for your job::

    .{{ proj_slug }}/jobs/<my_new_job>/__init__.py

Implement an *analyze* function within the module that accepts a SparkContext
as it's only argument::

    def analyze(sc):
        # your pyspark code here.

Add a module for your tests::

    ./tests/jobs/test_<my_new_job>.py

Add declarations to the sphinx api reference template to extract documentation::

    ./docs/api_reference.rst


    <Human readable job name>
    -------------------------

    .. automodule:: {{ proj_slug }}.jobs.<my_new_job>
        :members:
