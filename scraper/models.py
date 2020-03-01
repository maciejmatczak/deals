from django.db import models
from django.contrib.auth import get_user_model
from django.core import files
from django.core.exceptions import ValidationError
from django.urls import reverse
from croniter import croniter
from datetime import datetime
from solo.models import SingletonModel
from io import BytesIO
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


def validate_cron(value: str):
    try:
        croniter(value)
    except Exception as exception:
        raise ValidationError('Cron validation error: %(exception)s',
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
    cron = models.TextField(blank=False, validators=[
                            validate_cron], default='0 9 */1 * *')

    mail_me = models.BooleanField(default=False)

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


class JobRunner(SingletonModel):
    last_run = models.DateTimeField(default=datetime.utcnow)

    class Meta:
        verbose_name = "Job runner"


class Item(models.Model):
    identifier = models.TextField(blank=False, default='')
    url = models.URLField(blank=False)
    image = models.ImageField(upload_to='items', blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    scraping_job = models.ForeignKey(
        ScrapingJob, on_delete=models.SET_NULL, null=True)

    def get_absolute_image_url(self):
        return reverse('item-image', kwargs={'pk': self.pk})

    def recent_history(self):
        last_two_states = self.itemstate_set.order_by('-date_found')[0:2]

        if len(last_two_states) == 2:
            newer_state, older_state = last_two_states
        elif len(last_two_states) == 1:
            newer_state, older_state = last_two_states[0], None
        else:
            return None

        combined_keys = set()
        for state in last_two_states:
            data = state.data_as_dict()
            combined_keys |= set(k for k in data.keys() if data[k])
        combined_keys = sorted(combined_keys)

        if older_state:
            older_date_found = older_state.date_found
        else:
            older_date_found = ''

        recent_history = {
            'newer_date_found': newer_state.date_found,
            'older_date_found': older_date_found,
            'rest': []
        }

        for key in combined_keys:
            current_value = newer_state.data_as_dict().get(key, '')
            if older_state:
                older_value = older_state.data_as_dict().get(key, '')
            else:
                older_value = ''

            recent_history['rest'].append(
                {
                    'attribute': key,
                    'newer': current_value,
                    'older': older_value
                }
            )

        return recent_history


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
    def register(cls, scraping_job, scrapped_data, job_url):
        # scrapped data will consist characteristic items, as well as
        # some standard one

        identifier = scrapped_data.pop('identifier')
        url = scrapped_data.pop('url', None) or job_url
        image = scrapped_data.pop('image', None)

        item, _ = Item.objects.update_or_create(
            identifier=identifier,
            scraping_job=scraping_job,
            user=scraping_job.user,
            defaults={'url': url}
        )

        if image and type(image) == bytes:
            item.image.save(f'{identifier}.png', BytesIO(image))
            item.save()

        newest_state = cls.objects.order_by('-date_found').first()
        if not newest_state or newest_state.data_as_dict() != scrapped_data:
            _, created = cls.objects.get_or_create(
                item=item,
                data=yaml.dump(scrapped_data, default_flow_style=False,
                               allow_unicode=True)
            )
        else:
            created = False

        return created
