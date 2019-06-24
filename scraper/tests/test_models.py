import pytest
from scraper.models import ScrapingTask


pytestmark = pytest.mark.django_db


def test_user(user):
    assert user


def test_scrapting_task(user):
    user_email = user.email

    task = ScrapingTask(
        url='http://example.com',
        task='some task',
        running_time='10:00',
        user=user
    )

    assert task
    assert task.user.email == user_email
