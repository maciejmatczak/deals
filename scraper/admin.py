from django.contrib import admin

from .models import ScrapingTask, ScrapingJob, ScrapingJobLog, Item, ItemState

admin.site.register(ScrapingTask)
admin.site.register(ScrapingJob)
admin.site.register(ScrapingJobLog)
admin.site.register(Item)
admin.site.register(ItemState)
