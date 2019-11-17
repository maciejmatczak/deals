from django.contrib import admin

from .models import ScrapingTask, ScrapingJob, Item

admin.site.register(ScrapingTask)
admin.site.register(ScrapingJob)
admin.site.register(Item)
