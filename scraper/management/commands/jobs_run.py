from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime, time, timezone
from croniter import croniter
import yaml

from scraper.models import (
    ScrapingJob, ScrapingJobLog, ResultChoice, Item, ItemState, JobRunner)
from scraper.item_scraper import item_scraper
from scraper.item_scraper.item_scraper import (
    HTTPError
)
from scraper.item_scraper.validators import (
    ValidationError as ScrapTaskValidationError
)


def should_be_run(cron, after, before):
    iter_ = croniter(cron, after)
    next_ = iter_.get_next(datetime)
    return next_ <= before


def jobs_to_run(after: datetime, before: datetime):
    # jobs that are supposed to be run needs to be active, not yet run and
    # within apropriate time window
    # this approach might have some issues around midnight though, when all the
    # was_run_today fields should be resetted

    jobs = ScrapingJob.objects.filter(
        active=True,
    ).all()

    for job in jobs:
        if should_be_run(job.cron, after, before):
            yield job


class Command(BaseCommand):
    help = 'Runs scrap routines for every user and registers new items'

    def handle(self, *args, **options):
        now = datetime.now(timezone.utc)

        job_runner = JobRunner.get_solo()
        last_run = job_runner.last_run

        job_runner.last_run = now
        job_runner.save()

        self.stdout.write(
            f'Running scrap routine\n'
            f'   now: {now}\n'
            f'  last: {last_run}'
        )

        for scraping_job in jobs_to_run(after=last_run, before=now):
            self.stdout.write(
                f'Scraping {scraping_job} ({scraping_job.id})\n'
                f'  user: {scraping_job.user}\n'
                f'  cron: {scraping_job.cron}'
            )

            task = yaml.safe_load(scraping_job.scraping_task.task)

            try:
                results, page_source = item_scraper.scrap(
                    url=scraping_job.url,
                    task=task,
                    chromedriver_path=settings.SCRAPER_CHROMEDRIVER_PATH,
                    user_agent=settings.SCRAPER_USER_AGENT
                )
            except ScrapTaskValidationError as exception:
                ScrapingJobLog.objects.create(
                    scraping_job=scraping_job,
                    result=ResultChoice.INVALID_TASK,
                    result_info=str(exception)
                )
                self.stderr.write(
                    f'VALIDATION ERROR during scrapping:\n'
                    f'USER={scraping_job.user}\n'
                    f'JOB={scraping_job}\n'
                    f'TASK={task}\n'
                    f'EXCEPTION={exception}\n'
                )
                continue
            except HTTPError as exception:
                ScrapingJobLog.objects.create(
                    scraping_job=scraping_job,
                    result=ResultChoice.PAGE_UNAVAILABLE,
                    result_info=str(exception)
                )
                self.stderr.write(
                    f'HTTP ERROR during scrapping:\n'
                    f'USER={scraping_job.user}\n'
                    f'JOB={scraping_job}\n'
                    f'TASK={task}\n'
                    f'EXCEPTION={exception}\n'
                )
                continue
            finally:
                scraping_job.was_run_today = True
                scraping_job.save()

            self.stdout.write(self.style.SUCCESS(
                f'SCRAPPED {len(results)} results'))

            save_count = 0
            for result in results:
                created = ItemState.register(
                    scraping_job=scraping_job,
                    scrapped_data=result,
                    job_url=scraping_job.url
                )
                if created:
                    save_count += 1

            self.stdout.write(self.style.SUCCESS(
                f'SAVED {save_count} results'
            ))

            log_result = ResultChoice.OK_NONEW
            if save_count > 0:
                log_result = ResultChoice.OK_NEW

            ScrapingJobLog.objects.create(
                scraping_job=scraping_job,
                result=log_result
            )
