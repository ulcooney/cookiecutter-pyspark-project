#!/usr/bin/python
import argparse
import importlib
import time
import os
import sys

if os.path.exists('libs.zip'):
    sys.path.insert(0, 'libs.zip')
else:
    sys.path.insert(0, './libs')

if os.path.exists('jobs.zip'):
    sys.path.insert(0, 'jobs.zip')
else:
    sys.path.insert(0, './jobs')

# pylint:disable=E0401
try:
    import pyspark
except ImportError:
    import findspark
    findspark.init()
    import pyspark


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a PySpark job')
    parser.add_argument(
        '--job', type=str, required=True, dest='job_name',
        help="The name of the job module you want to run. (ex: poc will run job on jobs.poc package)")
    parser.add_argument(
        '--job-args', nargs='*',
        help="Extra arguments to send to the PySpark job (example: --job-args template=manual-email1 foo=bar")

    args = parser.parse_args()
    print(f"Called with arguments: {args}")

    environment = {
        'PYSPARK_JOB_ARGS': ' '.join(args.job_args) if args.job_args else ''
    }

    job_args = dict()
    if args.job_args:
        job_args_tuples = [arg_str.split('=') for arg_str in args.job_args]
        print('job_args_tuples: {job_args_tuples}')
        job_args = {a[0]: a[1] for a in job_args_tuples}

    print(f'Running job {args.job_name}...\nenvironment is {environment}')

    os.environ.update(environment)
    sc = pyspark.SparkContext(appName=args.job_name, environment=environment)
    job_module = importlib.import_module('{{cookiecutter.project_slug }}.jobs.%s' % args.job_name)

    start = time.time()
    job_module.analyze(sc, **job_args)
    end = time.time()

    duration = end - start
    print(f"Execution of job {args.job_name} took {duration} seconds")
