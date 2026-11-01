class CronError(ValueError):
    """Base class for every error this package raises."""


class InvalidCronFormatError(CronError):
    """The cron string does not have five fields followed by a command."""


class InvalidCronValueError(CronError):
    """A value in a field is outside that field's allowed range, or is not a number."""


class InvalidCyclicRangeError(CronError):
    """A range runs backwards (e.g. 5-2). Cyclic ranges are not supported."""
