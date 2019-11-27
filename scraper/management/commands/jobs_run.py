from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime, time
import yaml

from scraper.models import ScrapingJob, Item
from scraper.item_scraper import item_scraper
from scraper.item_scraper.validators import (
    ValidationError as ScrapTaskValidationError
)


def jobs_to_run(before: time):
    # jobs that are supposed to be run needs to be active, not yet run and
    # within apropriate time window
    # this approach might have some issues around midnight though, when all the
    # was_run_today fields should be resetted

    iterator = ScrapingJob.objects.filter(
        active=True,
        was_run_today=False,
        running_time__lte=before
    ).iterator()

    return iterator


class Command(BaseCommand):
    help = 'Runs scrap routines for every user and registers new items'

    def handle(self, *args, **options):
        now = datetime.now().time()

        self.stdout.write(
            f'Running scrap routine @ {now}'
        )

        for scraping_job in jobs_to_run(before=now):
            self.stdout.write(
                f'Scraping {scraping_job} ({scraping_job.id}) '
                f'for {scraping_job.user}'
            )

            task = yaml.safe_load(scraping_job.scraping_task.task)

            try:
                results, page_source = item_scraper.scrap(
                    url=scraping_job.url,
                    task=task,
                    chromedriver_path=settings.SCRAPER_CHROMEDRIVER_PATH
                )
            except ScrapTaskValidationError as exception:
                self.stderr.write(
                    f'ERROR during scrapping:\n'
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
                data = yaml.dump(result, default_flow_style=False,
                                 allow_unicode=True)

                if Item.objects.filter(
                    scraping_job__user=scraping_job.user,
                    data=data
                ).count() == 0:
                    item = Item(
                        data=data,
                        scraping_job=scraping_job
                    )
                    item.save()
                    save_count += 1

            self.stdout.write(self.style.SUCCESS(
                f'SAVED {save_count} results'))
