import pytest
from cron_parser.common.constants import COMMAND, DAY_OF_MONTH, DAY_OF_WEEK, MINUTE, HOUR, MONTH 
from cron_parser.common.exceptions import InvalidCronFormatError
from cron_parser.cron_parser import CronExpressionParser


def test_cron_expression_parser_valid_cron(yearly_cron_string):
    parser = CronExpressionParser(yearly_cron_string)
    
    expected_result = {
        MINUTE: 0,
        HOUR: 0,
        MONTH: 1,
        DAY_OF_MONTH: 1, 
        DAY_OF_WEEK: [1, 2,3,4,5,6,7],
        COMMAND: 'test_command'
    }

    result = parser.parse()

    assert expected_result == result


def test_cron_expression_parser_raises_invalid_cron_format_error(invalid_cron_string):
    parser = CronExpressionParser(invalid_cron_string)

    with pytest.raises(InvalidCronFormatError):
        parser.parse()
    

def test_cron_expression_parser_displays_cron_tab(yearly_cron_string, capsys):
    parser = CronExpressionParser(yearly_cron_string)

    result = parser.parse()

    parser.display_parsed_cron(result)

    captured_output = capsys.readouterr()

    expected_output = (
        "minute          0\n"
        "hour            0\n"
        "day of month    1\n"
        "month           1\n"
        "day of week     1 2 3 4 5 6 7\n"
        "command         test_command\n"
    )

    print(captured_output)

    assert expected_output == captured_output.out