from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import ScrapingTask, ScrapingJob, ScrapingJobLog, Item, ItemState, JobRunner

admin.site.register(ScrapingTask)
admin.site.register(ScrapingJob)
admin.site.register(ScrapingJobLog)
admin.site.register(Item)
admin.site.register(ItemState)
admin.site.register(JobRunner, SingletonModelAdmin)
