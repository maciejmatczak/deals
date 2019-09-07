import pytest
from scraper.models import ScrapingJob, ScrapingTask


pytestmark = pytest.mark.django_db


def test_user(user):
    assert user


def test_scraping_job(user, scraping_task):
    user_email = user.email

    task = ScrapingJob(
        url='http://example.com',
        scraping_task=scraping_task,
        running_time='10:00',
        user=user
    )

    assert task
    assert task.user.email == user_email


def test_scraping_jobs_for_user(user_factory, scraping_job_factory):
    user = user_factory.create()

    scraping_job_factory.create(user=user)
    scraping_job_factory.create(user=user)

    assert ScrapingJob.objects.filter(user=user).count() == 2, ScrapingJob.objects.all()
