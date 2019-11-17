from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import yaml

from scraper.models import ScrapingJob, Item
from scraper.item_scraper import item_scraper
from scraper.item_scraper.validators import ValidationError as ScrapTaskValidationError


class Command(BaseCommand):
    help = 'Runs scrap routines for every user and registers new items'

    def handle(self, *args, **options):
        for scraping_job in ScrapingJob.objects.filter(active=True).iterator():
            self.stdout.write(
                f'SCRAPPING {scraping_job} ({scraping_job.id}) '
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

            self.stdout.write(self.style.SUCCESS(
                f'SCRAPPED {len(results)} results'))

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
