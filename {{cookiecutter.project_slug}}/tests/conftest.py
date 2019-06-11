import logging

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--withspark", action="store_true", default=False,
        help="run tests requiring spark"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "spark: mark test as requiring spark")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--withspark"):
        return
    skip_spark = pytest.mark.skip(reason="need --withspark option to run")
    for item in items:
        if "spark" in item.keywords:
            item.add_marker(skip_spark)


def quiet_py4j():
    """ turn down spark logging for the test context """
    logger = logging.getLogger('py4j')
    logger.setLevel(logging.WARN)


@pytest.fixture(scope="session")
def spark_context(request):
    """
    Pytest fixture for creating a spark context
    """
    import findspark
    findspark.init()
    from pyspark import SparkConf
    from pyspark import SparkContext
    conf = (
        SparkConf().setMaster(
            "local[2]"
        ).setAppName(
            "pytest-pyspark-local-testing"
        )
    )
    sc = SparkContext(conf=conf)
    request.addfinalizer(lambda: sc.stop())

    quiet_py4j()
    return sc


@pytest.fixture(scope="session")
def hive_context(spark_context):
    """
    Fixture for creating a Hive Context
        tests in a session
    Args:
        spark_context: spark_context fixture

    Returns:
        HiveContext for tests

    """
    from pyspark import HiveContext
    return HiveContext(spark_context)


@pytest.fixture(scope="session")
def streaming_context(spark_context):
    """
    Fixture for creating a Streaming Context
        tests in a session
    Args:
        spark_context: spark_context fixture

    Returns:
        StreamingContext for tests

    """
    from pyspark.streaming import StreamingContext
    return StreamingContext(spark_context, 1)
