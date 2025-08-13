from django.db import models

# Create your models here.


class ProductType(models.Model):
    title = models.CharField(max_length=32, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_time"]


class ProductAttribute(models.Model):
    INTEGER = 1
    STRING = 2
    FLOAT = 3

    ATTRIBUTE_TYPES_FIELD = ((INTEGER, "Integer"), (STRING, "String"), (FLOAT, "Float"))

    title = models.CharField(max_length=32)
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="attributes"
    )
    attribute_type = models.PositiveSmallIntegerField(
        default=INTEGER, choices=ATTRIBUTE_TYPES_FIELD
    )

    def __str__(self):
        return self.title


class Brand(models.Model):
    name = models.CharField(max_length=32)
    parent = models.ForeignKey(
        "self", on_delete=models.PROTECT, related_name="children", blank=True, null=True
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=32)
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="categories",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="products"
    )
    upc = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    stock = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    is_active = models.BooleanField(default=True)

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products")

    def __str__(self):
        return self.title


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="attribute_values"
    )
    value = models.CharField(max_length=32)
    attribute = models.ForeignKey(
        ProductAttribute, on_delete=models.PROTECT, related_name="values"
    )

    def __str__(self):
        return self.value
