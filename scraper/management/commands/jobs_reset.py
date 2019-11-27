from django.core.management.base import BaseCommand

from scraper.models import ScrapingJob


class Command(BaseCommand):
    help = 'Resets jobs state of being already run'

    def handle(self, *args, **options):
        ScrapingJob.objects.all().update(was_run_today=False)
