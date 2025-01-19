import pytest
from cron_expression_parser.cron_field_expander import CronFieldExpander

def test_wildcard_expansion():
    expander = CronFieldExpander(0, 59)
    result = expander.expand("*")
    assert result == list(range(0, 60))

def test_range_expansion():
    expander = CronFieldExpander(0, 59)
    result = expander.expand("1-5")
    assert result == list(range(1,6))

def test_literal_expansion():
    expander = CronFieldExpander(0, 59)
    result = expander.expand("1")
    assert result == 1

def test_step_expansion():
    expander = CronFieldExpander(0,59)
    result = expander.expand("*/15")
    assert result == list(range(0, 60, 15))

def test_list_expansion():
    expander = CronFieldExpander(0, 59)
    result = expander.expand("1,15")
    assert result == [1, 15]
