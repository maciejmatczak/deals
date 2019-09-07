from django.contrib import admin

from .models import ScrapingTask, ScrapingJob, Product, Item

admin.site.register(ScrapingTask)
admin.site.register(ScrapingJob)
admin.site.register(Product)
admin.site.register(Item)
