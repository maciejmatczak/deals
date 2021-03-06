# Generated by Django 2.2.9 on 2019-12-22 18:45

from django.db import migrations, models
import scraper.models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0016_auto_20191222_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrapingjoblog',
            name='result',
            field=models.TextField(choices=[(scraper.models.ResultChoice('New results available'), 'New results available'), (scraper.models.ResultChoice('No new results available'), 'No new results available'), (scraper.models.ResultChoice('Invalid task'), 'Invalid task'), (scraper.models.ResultChoice('Page not available'), 'Page not available')]),
        ),
    ]
