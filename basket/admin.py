from django.contrib import admin
from basket.models import Basket, BasketLine
from django.contrib.admin import register


class BasketLineInline(admin.TabularInline):
    model = BasketLine


@register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_time']
    inlines = (BasketLineInline, )


