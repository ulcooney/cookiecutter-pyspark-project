============================
Cookiecutter Pyspark Project
============================

A Cookiecutter_ template for a basic project of Pyspark jobs.

Provides configuration for sphinx documentation and testing with pytest.

A docker stack for a pyspark / jupyter notebook container is also defined.
This allows for experimenting in notebooks and submitting jobs to be executed.

The resulting project is influenced by the following sources:

- https://medium.com/@GaryStafford/getting-started-with-pyspark-for-big-data-analytics-using-jupyter-notebooks-and-docker-ba39d2e3d6c7
- https://developerzen.com/best-practices-writing-production-grade-pyspark-jobs-cb688ac4d20f
- https://github.com/ekampf/PySpark-Boilerplate
- https://engblog.nextdoor.com/unit-testing-apache-spark-with-py-test-3b8970dc013b


The README within your newly created project contains a guide for development.


Usage
=====

You will need to have Cookiecutter_ installed::

    $ pip install cookiecutter


Clone this repository and then change to the directory in to which you would
like to create your new project. Then run the cookiecutter::

    $ cookiecutter /path/to/cookiecutter-pyspark-project


.. _Cookiecutter: https://github.com/audreyr/cookiecutter
