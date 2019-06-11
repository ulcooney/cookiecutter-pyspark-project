import re
from functools import partial
from {{ cookiecutter.project_slug }}.shared.context import JobContext


class WordCountDemoJobContext(JobContext):
    def _init_accumulators(self, sc):
        self.initalize_counter(sc, 'words')


strip_regexp = re.compile(r"[^\w]*")


def to_pairs(context, word):
    context.inc_counter('words')
    return word, 1


def analyze(sc):
    """
    An example job to perform a simple word count as a demonstration.

    :param SparkContext sc: A SparkContext_ instance.

    Each job module must define an *analyze* function that accepts a
    SparkContext and optional keyword arguments.

    To remove this example job from the project simply delete the following
    folders::

        ./pyspark_test_three/jobs/word_count_demo
        ./tests/jobs/word_count_demo

    And remove the references to *word_count_demo* in the sphinx documentation::

        ./docs/api_reference.rst

    .. _SparkContext: https://spark.apache.org/docs/2.1.0/api/python/pyspark.html#pyspark.SparkContext
    """
    context = WordCountDemoJobContext(sc)
    context.logger(sc).info('Running word count demo')

    text = get_text()

    to_pairs_trasform = partial(to_pairs, context)

    words = sc.parallelize(text.split())
    pairs = words.map(to_pairs_trasform)
    counts = pairs.reduceByKey(lambda a, b: a+b)
    ordered = counts.sortBy(lambda pair: pair[1], ascending=False)

    result = ordered.collect()
    context.print_accumulators()

    return result


def get_text():
    return 'demo text to analyze lorem ipsum blah etc'
