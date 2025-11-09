from django.contrib import admin 
from django.contrib.admin import register
from finance.models import Payment, GateWay

@register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ["invoice_number", "amount"]


@register(GateWay)
class GateWayModelAdmin(admin.ModelAdmin):
    list_display = ["title", "is_enable"]
