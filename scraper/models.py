from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
import yaml
from enum import Enum

User = get_user_model()


def validate_yaml(value):
    try:
        yaml.safe_load(value)
    except yaml.YAMLError as exception:
        raise ValidationError('Field is not a proper yaml: %(exception)s',
                              params={'exception': exception}
                              )


class ScrapingTask(models.Model):
    title = models.CharField(max_length=255, blank=False)
    favourite = models.BooleanField(default=True, blank=False)

    task = models.TextField(blank=False, validators=[validate_yaml])

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('scrapingtask-detail', kwargs={'pk': self.pk})


class ScrapingJob(models.Model):
    url = models.URLField(max_length=600, blank=False)
    active = models.BooleanField(default=True, blank=False)
    description = models.TextField(blank=True)
    running_time = models.TimeField(blank=False)
    was_run_today = models.BooleanField(default=False, blank=False)

    scraping_task = models.ForeignKey(
        ScrapingTask, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.url

    def get_absolute_url(self):
        return reverse('scrapingjob-detail', kwargs={'pk': self.pk})

    @property
    def last_log(self):
        if self.scrapingjoblog_set is not None and self.scrapingjoblog_set.count() > 0:
            return self.scrapingjoblog_set.first()
        else:
            return None


class ResultChoice(Enum):
    OK_NEW = 'New results available'
    OK_NONEW = 'No new results available'
    INVALID_TASK = 'Invalid task'
    PAGE_UNAVAILABLE = 'Page not available'


class ScrapingJobLog(models.Model):
    class Meta:
        ordering = ['-date_run']

    date_run = models.DateTimeField(auto_now_add=True)

    result = models.TextField(
        choices=((c, c.value) for c in ResultChoice)
    )
    result_info = models.TextField(blank=True)

    scraping_job = models.ForeignKey(
        ScrapingJob, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}: {self.result} @ {self.scraping_job}'


class Item(models.Model):
    identifier = models.TextField(blank=False, default='')

    scraping_job = models.ForeignKey(
        ScrapingJob, on_delete=models.SET_NULL, null=True)


class ItemState(models.Model):
    class Meta:
        ordering = ['-date_found']

    date_found = models.DateTimeField(auto_now_add=True)
    data = models.TextField(blank=False, validators=[validate_yaml])

    item = models.ForeignKey(
        Item, on_delete=models.SET_NULL, null=True)

    def data_as_dict(self):
        data = yaml.safe_load(self.data)

        for key in ['image', 'identifier']:
            try:
                data.pop(key)
            except KeyError:
                pass

        return data

    @classmethod
    def register(cls, scraping_job, scrapped_data):
        # scrapped data will consist characteristic items, as well as
        # some standard one

        identifier = scrapped_data.pop('identifier')
        image = scrapped_data.pop('image', None)

        item, _ = Item.objects.get_or_create(
            identifier=identifier,
            scraping_job=scraping_job
        )

        _, created = cls.objects.get_or_create(
            url=url,
            item=item,
            data=yaml.dump(scrapped_data, default_flow_style=False,
                           allow_unicode=True)
        )

        return created
