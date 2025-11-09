from faulthandler import is_enabled
from django.http import Http404
from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from finance.models import GateWay, Payment
from finance.utils.zarinpal import zpal_payment_checker, zpal_request_handler
from finance.forms import ChargeWalletForm


class ChargeWalletView(View):
    template_name = "finance/charge_wallet.html"
    form_class = ChargeWalletForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            payment_link, authority = zpal_request_handler(
                settings.ZARRINPAL["merchant_id"],
                form.cleaned_data["amount"],
                "Wallet-charge",
                "armin10gp@gmail.com",
                None,
                settings.ZARRINPAL["gateway_callback_url"],
            )

            if payment_link is not None:
                print(authority)
                print(payment_link)
                return redirect(payment_link)

        return render(request, self.template_name, {"form": form})


class VerifyView(View):
    template_name = "finance/callback.html"

    def get(self, request, *args, **kwargs):
        authority = request.GET.get("Authority")

        try:
            payment = Payment.objects.get(authority=authority)
        except Payment.DoesNotExist:
            raise Http404
        
        data = dict(merchant_id=payment.gateway.auth_data, amount=payment.amount, authority=payment.authority)
        payment.verify(data)

        return render(
            request, self.template_name, {"payment": payment}
        )


class PaymentView(View):

    def get(self, request, invoice_number, *args, **kwargs):
        try:
            payment = Payment.objects.get(invoice_number=invoice_number)
        except Payment.DoesNotExist:
            raise Http404

        gateway = GateWay.objects.filter(is_enable=True)
        return render(
            request,
            "finance/payment_detail.html",
            {"payment": payment, "gateways": gateway},
        )


class PaymentGatewayView(View):
    def post(self, request, invoice_number, gateway, *args, **kwargs):
        try:
            payment = Payment.objects.get(invoice_number=invoice_number)
        except Payment.DoesNotExist:
            raise Http404

        try:
            gateway = GateWay.objects.get(invoice_number=invoice_number)
        except Payment.DoesNotExist:
            raise Http404


        payment.gateway = gateway
        payment.save()
        payment_link = payment.bank_page
        if payment_link:
             return redirect(payment_link)
        

        gateway = GateWay.objects.filter(is_enable=True)
        return render(
            request,
            "finance/payment_detail.html",
            {"payment": payment, "gateways": gateway},
        )    


                    