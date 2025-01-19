# Onboarding Documentation for Cron Expression Service

This project providees a system for parsing and expanding cron expressions. The core functionality is split into two sub services: `CronFieldExpander` and `CronExpressionParser`. 

1. `CronFieldExpander`: This service expands the componetns for cron field (minute, hour, day etc)

2. `CronExpressionParser`: Handles parsing of a full cron expression and a command, expanding each field as necessary and provding an API to return a table so customers can see when their cron expressions run in a broken down manner..

The system supports the following cron expression components:

- Wildcards such as *
- Ranges (e.g. 1-5)
- Lists (e.g. 1,2,3)
- Steps (e.g. */5)

## Usage

To use the CronExpressionParser, you need to run the main.py script, passing a cron expression as an argument.

1. Command Syntax:

`python3 main.py <cron string>`

Example: `python3 main.py "30 2 * * * backup.sh"`

2. Output, this will display the expanded cron components like so:
```
minute          30
hour            2
day of month    1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31
month           1 2 3 4 5 6 7 8 9 10 11 12
day of week     1 2 3 4 5 6 7
command         backup.sh
```
The fields in the cron expression are expanded based on the supported formats: wildcards \*, ranges (1-5), lists (1,2,3), and steps (*/5).

## Cron Field definitions

- Literal: This returns the literal value provided by caller e.g. in the cron string, if there is a 1, this will return 1. 

- Wildcard: This is '*', and it gets expanded into all the range of possible values for that field, based on minumum and max values. For example, using wildcard on month will expand field to 1 2 3 4 5 6 7 8 9 10 11 12

- Range: This exapnds range values from start to stop. E.g. 1-5 in cron string expands to 1 2 3 4 5.

- Step: This expands the field in steps, from min value to max value. For example, * / 5. On minute, would return 0 5 10 15 ... 55



