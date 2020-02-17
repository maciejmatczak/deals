from django.apps import AppConfig


class ScraperConfig(AppConfig):
    name = 'scraper'

    def ready(self):
        import scraper.signals  # noqa
