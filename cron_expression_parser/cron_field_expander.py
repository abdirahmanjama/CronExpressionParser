from cron_expression_parser.common.exceptions import (
    InvalidCronValueError,
    InvalidCyclicRangeError,
)


class CronFieldExpander:
    """
    Expands one cron field (minute, hour, day of month, month or day of week)
    into the sorted list of concrete values it matches.

    A field is a comma-separated list of parts. Each part is one of:

        *          every value in the field's range
        5          a single value
        1-5        every value from 1 to 5 inclusive
        */15       every 15th value across the whole range
        1-10/2     every 2nd value from 1 to 10
        5/15       every 15th value from 5 to the end of the range

    Parts can be mixed in a list, so "1-3,7,*/20" is valid.
    """

    def __init__(self, min_value: int, max_value: int):
        self.min_value = min_value
        self.max_value = max_value

    def expand(self, field: str) -> list[int]:
        """Expand a field expression into a sorted, de-duplicated list of values."""
        values: set[int] = set()
        for part in field.split(","):
            values.update(self._expand_part(part))
        return sorted(values)

    def _expand_part(self, part: str) -> range:
        """Expand one comma-free part into a range of values."""
        if "/" in part:
            base, step_text = part.split("/", 1)
            step = self._to_int(step_text, part)
            if step <= 0:
                raise InvalidCronValueError(f"Step must be positive in '{part}'.")
        else:
            base, step = part, 1

        if base == "*":
            start, stop = self.min_value, self.max_value
        elif "-" in base:
            start_text, stop_text = base.split("-", 1)
            start, stop = self._to_int(start_text, part), self._to_int(stop_text, part)
        else:
            start = self._to_int(base, part)
            # "5/15" with no range means "from 5 to the end of the field".
            stop = self.max_value if step > 1 else start

        self._check_bounds(start, part)
        self._check_bounds(stop, part)
        if start > stop:
            raise InvalidCyclicRangeError(
                f"Invalid cyclic range {start}-{stop}. Cyclic ranges are currently not supported."
            )
        return range(start, stop + 1, step)

    def _to_int(self, text: str, part: str) -> int:
        try:
            return int(text)
        except ValueError:
            raise InvalidCronValueError(f"'{part}' is not a valid cron field.") from None

    def _check_bounds(self, value: int, part: str) -> None:
        if not self.min_value <= value <= self.max_value:
            raise InvalidCronValueError(
                f"'{part}' is out of range. Allowed values are {self.min_value}-{self.max_value}."
            )
