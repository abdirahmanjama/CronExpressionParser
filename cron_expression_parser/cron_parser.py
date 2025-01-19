from typing import Any, Union
from cron_expression_parser.common.exceptions import InvalidCronFormatError
from cron_expression_parser.common.constants import (
    MAX_DAY_OF_MONTH,
    MAX_DAY_OF_WEEK,
    MAX_HOUR,
    MAX_MINUTE,
    MAX_MONTH,
    MINUTE,
    HOUR,
    DAY_OF_MONTH,
    MONTH,
    DAY_OF_WEEK,
    COMMAND,
)
from cron_expression_parser.cron_field_expander import CronFieldExpander


class CronExpressionParser:
    """
    A class for parsing and expanding cron expressions.

    This class takes a cron string, parses it into its individual components (minute, hour, day of month, etc.),
    and expands wildcard characters, ranges, lists, and steps. It also provides functionality to display the parsed cron.
    """

    def __init__(self, cron_string: str):
        """
        Initialises the CronExpressionParser with the provided cron string.

        Args:
            cron_string (str): The cron expression to parse.
        """
        self.cron_string = cron_string
        self.parsed_cron = {}

    def parse(self) -> dict[str, Any]:
        """
        Parses the cron string and expands any fields with wildcards, ranges, lists, or steps.

        This method breaks down the cron expression into its individual components and expands the fields
        to their respective values.

        Returns:
            dict[str, Any]: A dictionary containing the expanded cron components (minute, hour, day of month, etc.).

        Raises:
            InvalidCronFormatError: If the cron string does not have exactly 6 components.
        """

        parts = self.cron_string.split(" ", 5)

        if len(parts) != 6:
            raise InvalidCronFormatError(
                f"Invalid Cron Format: {self.cron_string}. Must contain 5 fields and a command."
            )

        self.parsed_cron = {
            MINUTE: self._expand_field(parts[0], 0, MAX_MINUTE),
            HOUR: self._expand_field(parts[1], 0, MAX_HOUR),
            DAY_OF_MONTH: self._expand_field(parts[2], 1, MAX_DAY_OF_MONTH),
            MONTH: self._expand_field(parts[3], 1, MAX_MONTH),
            DAY_OF_WEEK: self._expand_field(parts[4], 1, MAX_DAY_OF_WEEK),
            COMMAND: parts[5],
        }

        return self.parsed_cron

    def display_parsed_cron(self, parsed_cron: dict[str, Any]) -> None:
        """
        Displays the parsed cron fields and their expanded values.

        Args:
            parsed_cron (dict[str, Any]): The dictionary containing the parsed cron fields.

        Prints each field and its corresponding expanded values to the console.
        """
        for field, values in parsed_cron.items():
            if isinstance(values, list):
                print(f"{field:<15} {' '.join(map(str, values))}")
            else:
                print(f"{field:<15} {values}")

    def _expand_field(
        self, field: str, min_value: int, max_value: int
    ) -> Union[list[int], Any, int]:
        """
        Expands the cron field based on the provided min and max values.

        Args:
            field (str): The expression to expand
            min_value (int): Theinimum value of this field
            max_value (int): The aximum value of this field

        Returns:
            Union[list[int], Any, int]: The expanded cron field, which could be a list of integers or a single integer.
        """
        expander = CronFieldExpander(min_value, max_value)
        expanded_field = expander.expand(field)
        return expanded_field
