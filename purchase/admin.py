from django.contrib import admin
from purchase.models import Purchase
from django.contrib.admin import register


@register(Purchase)
class PurchaseModelAdmin(admin.ModelAdmin):
    list_display = ["user", "package", "price", "status"]
    list_filter = ["status"]
