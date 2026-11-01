import sys

from cron_expression_parser.common.exceptions import CronError
from cron_expression_parser.cron_parser import CronExpressionParser


def main() -> None:
    if len(sys.argv) != 2:
        print('Usage: python3 main.py "<cron_string>"', file=sys.stderr)
        sys.exit(1)

    try:
        parser = CronExpressionParser(sys.argv[1])
        parser.display_parsed_cron(parser.parse())
    except CronError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
