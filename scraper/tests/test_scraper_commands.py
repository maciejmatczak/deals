import pytest
from datetime import time
from django.core.management import call_command

from scraper.management.commands.jobs_run import jobs_to_run
from scraper.models import ScrapingJob


@pytest.mark.django_db
def test_jobs_to_run(scraping_job_factory):

    job1 = scraping_job_factory.create(
        active=True,
        was_run_today=False,
        running_time=time(10, 20)
    )
    job2 = scraping_job_factory.create(
        active=False,
        was_run_today=False,
        running_time=time(10, 30)
    )
    job3 = scraping_job_factory.create(
        active=True,
        was_run_today=False,
        running_time=time(10, 40)
    )
    job4 = scraping_job_factory.create(
        active=True,
        was_run_today=False,
        running_time=time(10, 41)
    )

    job5 = scraping_job_factory.create(
        active=True,
        was_run_today=True,
        running_time=time(10, 20)
    )

    # Before 10:40 there should be 2 jobs to run, as one is inactive
    jobs = list(jobs_to_run(time(10, 40)))
    assert {job1.id, job3.id} == set(j.id for j in jobs)

    # Let's update the state of the jobs that were already run
    for job in jobs:
        job.was_run_today = True
        job.save()

    # Five minutes later we should get one job...
    jobs = list(jobs_to_run(time(10, 45)))
    assert {job4.id} == set(j.id for j in jobs)

    for job in jobs:
        job.was_run_today = True
        job.save()

    # at the end of the day we should no jobs to run
    jobs = jobs_to_run(time(23, 55))
    assert set() == set(j.id for j in jobs)

    # so as we reset the jobs and test one more time, jobs should be available
    # again
    call_command('jobs_reset')

    jobs = jobs_to_run(time(10, 45))
    assert {job1.id, job3.id, job4.id, job5.id} == set(j.id for j in jobs)
