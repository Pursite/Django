from django.shortcuts import render
from django.http import HttpResponse
from catalogue.models import Product, Category
from django.db.models import Q


def Product_list(request):
    products = Product.objects.select_related("category").all()
    context = "\n".join([f"{product.title} {product.upc}, {product.category.name} " for product in products])
    return HttpResponse(context)


def Product_detail(request, pk):
    queryset = Product.objects.filter(is_active=True).filter(Q(pk=pk) | Q(upc=pk))
    if queryset.exists():
        product = queryset.first()
        return HttpResponse(f"title : {product.title}")
    return HttpResponse("Product does not exist")


def category_products(request, pk):
    try:
        category = Category.objects.prefetch_related("products").get(pk=pk)
    except Category.Doesnotexsits:
        return HttpResponse("category does not exists")
