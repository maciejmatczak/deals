import pytest
from datetime import time, datetime, timezone
from django.core.management import call_command

from scraper.management.commands.jobs_run import jobs_to_run, should_be_run
from scraper.models import ScrapingJob


@pytest.mark.parametrize(
    'cron, after, before', (
        ('34 9 */1 * *', datetime(2020, 1, 1, 9, 30), datetime(2020, 1, 1, 9, 35)),
        ('35 9 */1 * *', datetime(2020, 1, 1, 9, 30), datetime(2020, 1, 1, 9, 35)),
        ('34 9 */2 * *', datetime(2020, 1, 1, 9, 30), datetime(2020, 1, 1, 9, 35)),
    )
)
def test_should_be_run(cron, after, before):
    assert should_be_run(cron, after, before)


@pytest.mark.parametrize(
    'cron, after, before', (
        ('30 9 */1 * *', datetime(2020, 1, 1, 9, 30), datetime(2020, 1, 1, 9, 35)),
        (' 0 9 */1 * *', datetime(2020, 1, 1, 9, 30), datetime(2020, 1, 1, 9, 35)),
        ('34 9 */2 * *', datetime(2020, 1, 2, 9, 30), datetime(2020, 1, 2, 9, 35)),
    )
)
def test_should_be_run_not(cron, after, before):
    assert not should_be_run(cron, after, before)
