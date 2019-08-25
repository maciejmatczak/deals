from django.contrib import admin

from .models import ScrapingJob, Product, Item

admin.site.register(ScrapingJob)
admin.site.register(Product)
admin.site.register(Item)
