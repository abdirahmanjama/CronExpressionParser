#!/bin/bash
set -e
pytest --cov=cron_expression_parser --cov-report=term-missing tests/
