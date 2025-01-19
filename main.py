import sys
from cron_expression_parser.cron_parser import CronExpressionParser
from cron_expression_parser.common.exceptions import InvalidCronFormatError

def main():
    if len(sys.argv) != 2:
        print('Usage: python3 main.py "<cron_string>"')
        sys.exit(1)

    cron_string = sys.argv[1]

    try:
        parser = CronExpressionParser(cron_string)
        parsed_cron = parser.parse()
        parser.display_parsed_cron(parsed_cron) 
    except InvalidCronFormatError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
