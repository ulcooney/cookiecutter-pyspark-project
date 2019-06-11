from unittest.mock import patch, MagicMock

import pytest

from {{ cookiecutter.project_slug }}.jobs.word_count_demo import analyze, to_pairs


def test_to_pairs():
    context = MagicMock()

    result = to_pairs(context, 'foo')

    context.inc_counter.assert_called_with('words')
    assert result[0] == 'foo'
    assert result[1] == 1


@pytest.mark.spark
@patch('{{ cookiecutter.project_slug }}.jobs.word_count_demo.get_text')
def test_wordcount(get_text_mock, spark_context):
    get_text_mock.return_value = "foo bar foo"

    result = analyze(spark_context)

    assert result[0] == ('foo', 2)
    assert result[1] == ('bar', 1)
