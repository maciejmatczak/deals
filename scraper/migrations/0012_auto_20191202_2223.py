# Generated by Django 2.2.7 on 2019-12-02 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0011_item_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='identifier',
            field=models.TextField(null=True),
        ),
    ]
