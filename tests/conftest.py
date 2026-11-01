import pytest


@pytest.fixture
def yearly_cron_string():
    return "0 0 1 1 * test_command"


@pytest.fixture
def invalid_cron_string():
    return "clearly not cron"
