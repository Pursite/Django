from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from basket.models import Basket
from catalogue.models import Product
from django.http import Http404
from basket.forms import AddToBasketFrom

    # TODO: Define form fields here



@require_POST
def add_to_pasket(request):
    response = HttpResponseRedirect(request.POST.get('next', '/'))

    basket = Basket.get_basket(request.COOKIE.get('basket_id', None))
    if basket is None:
        raise Http404
    # if basket_id is None:
    #     basket = Basket.objects.create()
    #     response.set_cookie('basket_id', basket.id)
    # else:
    #     try:
    #         basket = Basket.objects.get(pk=basket_id)
    #     except Basket.DoesNotExist:
    #         raise Http404
    response.set_cookie('basket_id', basket.id)

    if not basket.validate_user(request.user):
        raise Http404
    
    form = AddToBasketFrom(request.POST)
    if form.is_valid():
        form.save(basket=basket)
    
    # product_id = request.POST.get('product_id', None)
    # quantity = request.POST.get('quantity', 1)
    # try:
    #     quantity = int(quantity)
    # except:
    #     quantity = 1
    # if product_id is not None:
    #     try:
    #         product = Product.objects.get(pk=product_id)
    #     except Product.DoesNotExist:
    #         raise Http404
    #     else:
    #         basket.add(product, quantity)

    return response