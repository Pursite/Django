from django.urls import path
from .views import *

urlpatterns = [
    path("product/list/", Product_list, name="Product-list"),
    path("product/detail/<int:pk>/", Product_detail, name="Product-detail"),
    path("category/<int:pk/products/>", category_products)
]