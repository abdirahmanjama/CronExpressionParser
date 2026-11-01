import pytest

from cron_expression_parser.common.constants import (
    COMMAND,
    DAY_OF_MONTH,
    DAY_OF_WEEK,
    MINUTE,
    HOUR,
    MONTH,
)
from cron_expression_parser.common.exceptions import (
    InvalidCronFormatError,
    InvalidCronValueError,
)
from cron_expression_parser.cron_parser import CronExpressionParser


def test_cron_expression_parser_valid_cron(yearly_cron_string):
    result = CronExpressionParser(yearly_cron_string).parse()

    assert result == {
        MINUTE: [0],
        HOUR: [0],
        DAY_OF_MONTH: [1],
        MONTH: [1],
        DAY_OF_WEEK: [1, 2, 3, 4, 5, 6, 7],
        COMMAND: "test_command",
    }


def test_the_example_from_the_task():
    result = CronExpressionParser("*/15 0 1,15 * 1-5 /usr/bin/find").parse()

    assert result[MINUTE] == [0, 15, 30, 45]
    assert result[HOUR] == [0]
    assert result[DAY_OF_MONTH] == [1, 15]
    assert result[MONTH] == list(range(1, 13))
    assert result[DAY_OF_WEEK] == [1, 2, 3, 4, 5]
    assert result[COMMAND] == "/usr/bin/find"


def test_command_keeps_its_own_spaces():
    result = CronExpressionParser("* * * * * echo hello world").parse()
    assert result[COMMAND] == "echo hello world"


def test_extra_whitespace_between_fields_is_tolerated():
    result = CronExpressionParser("  0   0  1 1  *   test_command").parse()
    assert result[COMMAND] == "test_command"
    assert result[MINUTE] == [0]


def test_raises_invalid_cron_format_error(invalid_cron_string):
    with pytest.raises(InvalidCronFormatError):
        CronExpressionParser(invalid_cron_string).parse()


def test_raises_when_a_field_is_out_of_range():
    with pytest.raises(InvalidCronValueError):
        CronExpressionParser("60 0 1 1 * test_command").parse()


def test_displays_cron_as_a_table(yearly_cron_string, capsys):
    parser = CronExpressionParser(yearly_cron_string)
    parser.display_parsed_cron(parser.parse())

    assert capsys.readouterr().out == (
        "minute        0\n"
        "hour          0\n"
        "day of month  1\n"
        "month         1\n"
        "day of week   1 2 3 4 5 6 7\n"
        "command       test_command\n"
    )
