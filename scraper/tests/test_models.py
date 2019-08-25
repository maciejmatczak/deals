import pytest
from scraper.models import ScrapingJob


pytestmark = pytest.mark.django_db


def test_user(user):
    assert user


def test_scraping_job(user):
    user_email = user.email

    task = ScrapingJob(
        url='http://example.com',
        task='some task',
        running_time='10:00',
        user=user
    )

    assert task
    assert task.user.email == user_email
