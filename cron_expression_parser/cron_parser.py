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

# (field name, minimum, maximum) in the order they appear in a cron string.
FIELDS = (
    (MINUTE, 0, MAX_MINUTE),
    (HOUR, 0, MAX_HOUR),
    (DAY_OF_MONTH, 1, MAX_DAY_OF_MONTH),
    (MONTH, 1, MAX_MONTH),
    (DAY_OF_WEEK, 1, MAX_DAY_OF_WEEK),
)

ParsedCron = dict[str, list[int] | str]


class CronExpressionParser:
    """
    Parses a cron string of five time fields and a command, and expands each
    time field into the concrete values it matches.
    """

    def __init__(self, cron_string: str):
        self.cron_string = cron_string
        self.parsed_cron: ParsedCron = {}

    def parse(self) -> ParsedCron:
        """
        Split the cron string into its five time fields and the command, and
        expand each time field.

        Raises:
            InvalidCronFormatError: if there are not five fields and a command.
            InvalidCronValueError: if a field contains a value outside its range.
            InvalidCyclicRangeError: if a range runs backwards.
        """
        # split(None, 5) treats any run of whitespace as one separator and
        # keeps everything after the fifth field together as the command.
        parts = self.cron_string.split(None, 5)

        if len(parts) != 6:
            raise InvalidCronFormatError(
                f"Invalid Cron Format: '{self.cron_string}'. Must contain 5 fields and a command."
            )

        self.parsed_cron = {
            name: CronFieldExpander(lo, hi).expand(token)
            for (name, lo, hi), token in zip(FIELDS, parts[:5])
        }
        self.parsed_cron[COMMAND] = parts[5]
        return self.parsed_cron

    @staticmethod
    def format_parsed_cron(parsed_cron: ParsedCron) -> str:
        """Render the parsed cron as a table: field name, 14 columns wide, then values."""
        lines = []
        for field, values in parsed_cron.items():
            rendered = values if isinstance(values, str) else " ".join(map(str, values))
            lines.append(f"{field:<14}{rendered}")
        return "\n".join(lines)

    def display_parsed_cron(self, parsed_cron: ParsedCron) -> None:
        """Print the parsed cron as a table."""
        print(self.format_parsed_cron(parsed_cron))
