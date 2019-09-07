# Generated by Django 2.1.5 on 2019-08-25 17:03

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    # django.db.utils.NotSupportedError: Renaming the 'scraper_scrapingtask'
    # table while in a transaction is not supported on SQLite because it would
    # break referential integrity. Try adding `atomic = False` to the Migration
    # class.
    atomic = False

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scraper', '0003_auto_20190825_1856'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ScrapingTask',
            new_name='ScrapingJob',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='scraping_task',
            new_name='scraping_job',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='scraping_task',
            new_name='scraping_job',
        ),
    ]