# Generated by Django 2.1.5 on 2019-08-31 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import scraper.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scraper', '0004_auto_20190825_1903'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapingTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.TextField(validators=[scraper.models.validate_yaml])),
                ('favourite', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='scrapingjob',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraper.ScrapingTask'),
        ),
    ]
