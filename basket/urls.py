from django.urls import path
from basket.views import add_to_pasket


urlpatterns = [
    path('add/', add_to_pasket, name="add-to-basket")
]