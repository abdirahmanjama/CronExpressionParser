# Cron expression parser

A take-home task that comes up at a lot of UK companies, worked through end to end. This is my solution, and the one referenced in the **Big Tech Interview Prep Guide** from [The Software Club](https://skool.com/softwareclub). Do the task yourself first, under time, then compare.

## The task

Write a command-line program that takes one argument: a standard cron line with five time fields (minute, hour, day of month, month, day of week) followed by a command. Expand each field to show the times at which it will run, and print a table with the field name in a 14-character left-aligned column followed by the values.

```
$ python3 main.py "*/15 0 1,15 * 1-5 /usr/bin/find"
minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find
```

Special strings like `@yearly` are out of scope.

## Run it

Python 3.10 or newer, no dependencies.

```
python3 main.py "<cron string>"
```

## Test it

```
pip install -r requirements.txt
pytest
```

`./run_tests.sh` runs the same suite with a coverage report.

## How it's put together

```
main.py                                   CLI: argument handling and exit codes
cron_expression_parser/
  cron_parser.py                          splits the line into fields and a command
  cron_field_expander.py                  expands one field ("*/15", "1-5,7") into values
  common/constants.py                     field names and ranges
  common/exceptions.py                    one error type per thing that can go wrong
tests/                                    one test per input shape, plus the error cases
docs/edge_cases.md                        what the spec leaves open and what this does about it
```

## Decisions the spec leaves to you

1. **Out-of-range values** (minute `60`, month `13`) are rejected with a clear message and a non-zero exit code, not silently accepted.
2. **A single value with a step** (`5/15`) means "from 5 to the end of the field", which is how most cron implementations read it.
3. **Backward ranges** (`5-2`) are rejected. Some crons treat them as wrapping around; this one does not, and says so.
4. **Day of week is 1–7.** The spec doesn't say; `docs/edge_cases.md` discusses switching to 0–6.
5. **Extra whitespace** between fields is tolerated, and the command keeps its own internal spaces.

Noticing that these are missing from the spec, choosing, and writing the choice down is a large part of what a reviewer is looking for.
