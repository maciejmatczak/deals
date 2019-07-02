from django.contrib import admin

from .models import ScrapingTask, Product, Item

admin.site.register(ScrapingTask)
admin.site.register(Product)
admin.site.register(Item)
