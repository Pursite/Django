from django.contrib import admin
from django.contrib.admin import register
from .models import ShippingAddres


@register(ShippingAddres)
class ShippingAddresAdmin(admin.ModelAdmin):
    list_display = ["user", "city", "zip_code", "created_time"]
