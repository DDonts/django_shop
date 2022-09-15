from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Item, Order


@admin.register(Item)
class ItemAdmin(ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ['total']
