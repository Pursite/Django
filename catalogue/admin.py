from django.contrib import admin
from django.contrib.admin import register
from .models import (
    Category,
    Brand,
    Product,
    ProductType,
    ProductAttribute,
    ProductAttributeValue,
)


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


class ProductAttributeValueInLine(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1


@register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "upc",
        "product_type",
        "is_active",
        "stock",
        "title",
        "category",
        "brand",
    ]
    list_display_links = ["upc", "product_type"]
    list_filter = ["is_active"]
    search_fields = ["upc", "title", "category__name", "brand__name"]
    list_editable = ["is_active"]
    ordering = ["-upc"]
    inlines = [ProductAttributeValueInLine]


@register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]
    inlines = [ProductAttributeInline]


@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent"]
    search_fields = ["name"]
    list_filter = ["parent"]
    ordering = ["name"]


@register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "parent"]
    search_fields = ["name"]
    list_filter = ["parent"]
    ordering = ["name"]
