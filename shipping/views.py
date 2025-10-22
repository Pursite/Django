from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods, require_GET
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shipping.forms import ShippingAddressForm
from shipping.models import ShippingAddres
from django.views.generic import ListView, FormView
from django.utils.decorators import method_decorator


@login_required
@require_GET
def address_list(request):
        address = ShippingAddres.objects.filter(user=request.user)
        return render(request, 'shipping/list.html', {'address': address})


# class AddressListView(View):
#     @method_decorator(login_required) 
#     def get(self, request):                                                    first sample
#         address = ShippingAddres.objects.filter(user=request.user)
#         return render(request, 'shipping/list.html', {'address': address})


 
class CustomUserListView(ListView):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class AddressListView(CustomUserListView):
    model = ShippingAddres
    template_name = 'shipping/list.html'
    context_object_name = 'address'
    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs) 
        context['extra_data'] = self.get_queryset().count()
        return context
    

@login_required
@require_http_methods(request_method_list=['GET', 'POST'])
def address_create(request):
    if request.method == "POST":
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect("address-list")

    else: 
        form = ShippingAddressForm()
    return render(request, "shipping/create.html", {'form': form})


class AddressCreateView(FormView):
    form_class = ShippingAddressForm
    template_name = 'shipping/create.html'
    # success_url = '/shipping/list/'
    success_url = reverse_lazy('address-list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()    
        return super().form_valid(form)
    