from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
import yaml


User = get_user_model()


def validate_yaml(value):
    try:
        yaml.safe_load(value)
    except yaml.YAMLError as exception:
        raise ValidationError('Field is not a proper yaml: %(exception)s',
                              params={'exception': exception}
                              )


class ScrapingTask(models.Model):
    url = models.URLField(max_length=600, blank=False)
    active = models.BooleanField(default=True, blank=False)
    multiple = models.BooleanField(default=False, blank=False)
    task = models.TextField(blank=False, validators=[validate_yaml])
    description = models.TextField(blank=True)
    running_time = models.TimeField(blank=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.url

    def get_absolute_url(self):
        return reverse('scrapingtask-detail', kwargs={'pk': self.pk})


class Product(models.Model):
    name = models.TextField(blank=False)
    url = models.URLField(max_length=600, blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
    image_url = models.URLField(blank=False)

    date_found = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    scraping_task = models.ForeignKey(ScrapingTask, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Item(models.Model):
    data = models.TextField(blank=False, validators=[validate_yaml])
    scraping_task = models.ForeignKey(ScrapingTask, on_delete=models.SET_NULL, null=True)
