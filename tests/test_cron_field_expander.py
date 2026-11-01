import pytest

from cron_expression_parser.common.exceptions import (
    InvalidCronValueError,
    InvalidCyclicRangeError,
)
from cron_expression_parser.cron_field_expander import CronFieldExpander


@pytest.fixture
def minutes():
    return CronFieldExpander(0, 59)


def test_wildcard_expansion(minutes):
    assert minutes.expand("*") == list(range(0, 60))


def test_literal_expansion(minutes):
    assert minutes.expand("1") == [1]


def test_range_expansion(minutes):
    assert minutes.expand("1-5") == [1, 2, 3, 4, 5]


def test_step_on_wildcard(minutes):
    assert minutes.expand("*/15") == [0, 15, 30, 45]


def test_step_on_range(minutes):
    assert minutes.expand("1-10/2") == [1, 3, 5, 7, 9]


def test_step_on_single_value_runs_to_end_of_range():
    assert CronFieldExpander(0, 7).expand("3/2") == [3, 5, 7]


def test_list_expansion(minutes):
    assert minutes.expand("1,15") == [1, 15]


def test_list_can_mix_ranges_steps_and_values(minutes):
    assert minutes.expand("1-3,7,*/20") == [0, 1, 2, 3, 7, 20, 40]


def test_duplicates_are_removed_and_sorted(minutes):
    assert minutes.expand("5,1-5,3") == [1, 2, 3, 4, 5]


@pytest.mark.parametrize("field", ["60", "0-60", "*/0", "a", "1-b", "5--7"])
def test_out_of_range_or_malformed_values_are_rejected(minutes, field):
    with pytest.raises(InvalidCronValueError):
        minutes.expand(field)


def test_backward_range_is_rejected(minutes):
    with pytest.raises(InvalidCyclicRangeError):
        minutes.expand("5-2")
