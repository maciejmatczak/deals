from django.contrib import admin

from .models import ScrapingTask, Product

admin.site.register(ScrapingTask)
admin.site.register(Product)
