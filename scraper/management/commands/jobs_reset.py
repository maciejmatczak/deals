from django.core.management.base import BaseCommand

from scraper.models import ScrapingJob


class Command(BaseCommand):
    help = 'Runs scrap routines for every user and registers new items'

    def handle(self, *args, **options):
        ScrapingJob.objects.all().update(was_run_today=False)
