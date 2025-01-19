from cron_expression_parser.common.exceptions import InvalidCyclicRangeError


class CronFieldExpander:
    """
    A class to expand cron field expressions into their respective values
    At the moment, we only support expansions for wildcards, ranges, steps and lists.
    """

    def __init__(self, min_value, max_value):
        """
        Initializes the CronFieldExpander instance with a range of values.

        Args:
            min_value (int): The minimum value for the cron field.
            max_value (int): The maximum value for the cron field.
        """
        self.min_value = min_value
        self.max_value = max_value

    def expand(self, field: str):
        """
        Expands a single cron field (minute, hour, day, etc.) based on the given min and max values.

        Args:
            field (str): The cron field to expand.
            min_value (int): The minimum value for the field.
            max_value (int): The maximum value for the field.

        Returns:
            Union[list[int], int]: The expanded cron field, which could be a list of integers or a single integer.
        """
        operator_handlers = {
            "-": self._handle_range,
            ",": self._handle_list,
            "/": self._handle_step,
        }

        if field == "*":
            return self._handle_wildcard()

        for operator, handler in operator_handlers.items():
            if operator in field:
                if operator in ["-", ","]:
                    return handler(field)
                return handler(field)

        return self._handle_literal(field)

    def _handle_wildcard(self) -> list[int]:
        """
        Expands a wildcard '*' to a list of all values from min_value to max_value.

        Args:
            min_value (int): The minimum value of the field.
            max_value (int): The maximum value of the field.

        Returns:
            list[int]: A list of values from min_value to max_value.
        """
        return list(range(self.min_value, self.max_value + 1))

    def _handle_step(self, field) -> list[int]:
        """
        Expands a step expression (e.g., '*/5') to a list of values from min_value to max_value.

        Args:
            field (str): The step expression to expand (e.g., "*/5").
            min_value (int): The minimum value of the field.
            max_value (int): The maximum value of the field.

        Returns:
            list[int]: A list of values based on the step expression.
        """
        base, step = field.split("/")
        base = self.min_value if base == "*" else int(base)
        step = int(step)
        return list(range(base, self.max_value + 1, step))

    def _handle_list(self, field: str) -> list[int]:
        """
        Expands a list expression (e.g., '1,2,3') to a list of integers.

        Args:
            field (str): The list expression to expand (e.g., "1,2,3").

        Returns:
            list[int]: A list of integers from the list expression.
        """
        return [int(value) for value in field.split(",")]

    def _handle_literal(self, field: str) -> int:
        """
        Returns a literal value as an integer.

        Args:
            field (str): The literal value to return.

        Returns:
            int: The integer representation of the literal value.
        """
        return int(field)

    def _handle_range(self, field: str) -> list[int]:
        """
        Expands a range expression (e.g., '1-5') to a list of integers.

        Args:
            field (str): The range expression to expand (e.g., "1-5").

        Returns:
            list[int]: A list of integers from the start to the stop of the range.
        """
        start, stop = map(int, field.split("-"))

        if start > stop:
            raise InvalidCyclicRangeError(
                f"Invalid cyclic range {start}-{stop}. Cyclic ranges are currently not supported."
            )
        return list(range(start, stop + 1))
