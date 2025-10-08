from django.shortcuts import render
from django.http import HttpResponse, Http404
from catalogue.models import Product, Category
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from .utils import check_is_active, check_is_staff
from basket.forms import AddToBasketFrom

def product_list(request):
    context = dict()
    context["products"] = Product.objects.select_related("category").all()
    # return HttpResponse(context)
    return render(request, "catalogue/product_list.html", context=context)

def product_detail(request, pk):
    queryset = Product.objects.filter(is_active=True).filter(Q(pk=pk) | Q(upc=pk))
    if queryset.exists():
        product = queryset.first()
        form = AddToBasketFrom({'product': product.id, 'quantity': 1})
        return render(request, "catalogue/product_detail.html", {"product": product, "form": form})
    raise Http404


def category_products(request, pk):
    try:
        category = Category.objects.prefetch_related("products").get(pk=pk)
    except Category.Doesnotexsits:
        return HttpResponse("category does not exists")


def product_search(request):
    title = request.GET.get("q")
    products = (
        Product.objects.filter(is_active=True)
        .filter(title__icontains=title)
        .filter(category__name__icontains=title)
        .filter(category__is_active=True)
        .distinct()
    )
    context = "\n".join([f"{product.title} {product.upc}" for product in products])
    return HttpResponse(f"Search page:\n{context}")


@require_http_methods(request_method_list=["POST", "GET"])
@login_required
# @user_passes_test(check_is_active)
@permission_required("")
def user_profile(request):
    return HttpResponse(f"hello {request.user.username}")


# @require_GET
@require_POST
@login_required
@user_passes_test(lambda u: u.score > 20)
@user_passes_test(lambda u: u.age > 14)
def campaign(request):
    return HttpResponse(f"hello {request.user.username}")


