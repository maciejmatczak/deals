from django import forms
from django.db import models

from .models import ScrapingJob, ScrapingTask


class ScrapingJobCreateForm(forms.ModelForm):
    class Meta:
        model = ScrapingJob
        fields = [
            'url',
            'active',
            'multiple',
            'scraping_task',
            'running_time',
            'description'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scraping_task'].queryset = \
            ScrapingTask.objects.filter(user=self.instance.user)


class ScrapingJobUpdateForm(forms.ModelForm):
    class Meta:
        model = ScrapingJob
        fields = [
            'url',
            'active',
            'multiple',
            'scraping_task',
            'running_time',
            'description'
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scraping_task'].queryset = \
            ScrapingTask.objects.filter(user=self.instance.user)
