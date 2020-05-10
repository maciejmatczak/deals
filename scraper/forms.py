from django import forms
from django.forms.models import modelformset_factory

from .models import ScrapingJob, ScrapingTask


class ScrapingJobForm(forms.ModelForm):
    class Meta:
        model = ScrapingJob
        fields = [
            'url',
            'active',
            'mail_me',
            'scraping_task',
            'cron',
            'description'
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'cron': forms.Textarea(attrs={'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['scraping_task'].queryset = \
            ScrapingTask.objects.filter(user=self.current_user)


ScrapingJobSimpleFormSet = modelformset_factory(
    ScrapingJob,
    fields=[
        'active',
        'mail_me'
    ],
    extra=0,
    widgets={
        'active': forms.CheckboxInput(attrs={'onchange': 'submit();'}),
        'mail_me': forms.CheckboxInput(attrs={'onchange': 'submit();'}),
    }
)
