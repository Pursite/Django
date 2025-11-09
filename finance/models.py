import uuid
import json

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from finance.utils.zarinpal import zpal_payment_checker, zpal_request_handler


class GateWay(models.Model):
    FUNCTION_SAMAN = 'saman'
    FUNCTION_SHAPARAK = 'shaparak'
    FUNCTION_FINOTECH = 'finotech'
    FUNCTION_ZARRINPAL = 'zarrinpal'
    FUNCTION_PERSIAN = 'persian'
    GATEWAY_FUNCTIONS = (
        (FUNCTION_SAMAN, _('Saman')),
        (FUNCTION_SHAPARAK, _('Shaparak')),
        (FUNCTION_FINOTECH, _('Finotech')),
        (FUNCTION_ZARRINPAL, _('Zarrinpal')),
        (FUNCTION_PERSIAN, _('Persian')),

    )

    title = models.CharField(max_length=100, verbose_name=_("gateway title"))
    gateway_request_url = models.CharField(max_length=150, verbose_name=_("request url"), null=True, blank=True)
    gateway_verify_url = models.CharField(max_length=150, verbose_name=_("verify url"), null=True, blank=True)
    gateway_code = models.CharField(max_length=12, verbose_name=_("gateway code"), choices=GATEWAY_FUNCTIONS)
    is_enable = models.BooleanField(_('is enable'), default=True)
    auth_data = models.TextField(verbose_name=_("auth data"), null=True, blank=True)

    class Meta:
        verbose_name = _("Gateway")
        verbose_name_plural = _("Gateways")

    def __str__(self):
        return self.title
    
    def get_request_handler(self):
        handlers = {
            self.FUNCTION_SAMAN: None,
            self.FUNCTION_SHAPARAK: None,
            self.FUNCTION_PERSIAN: None,
            self.FUNCTION_FINOTECH: None,
            self.FUNCTION_ZARRINPAL: zpal_request_handler,
        }
        return handlers[self.gateway_code]
    

    def get_verify_handler(self):
        handlers = {
            self.FUNCTION_SAMAN: None,
            self.FUNCTION_SHAPARAK: None,
            self.FUNCTION_PERSIAN: None,
            self.FUNCTION_FINOTECH: None,
            self.FUNCTION_ZARRINPAL: zpal_payment_checker,
        }
        return handlers[self.gateway_code]
    
    @property
    def credentials(self):
        return json.loads(self.auth_data)
    


class Payment(models.Model):
    invoice_number = models.UUIDField(verbose_name=_("invoice number"), unique=True, default=uuid.uuid4)
    amount = models.PositiveIntegerField(verbose_name=_("payment amount"), editable=True)
    gateway = models.ForeignKey(GateWay, related_name="payments", null=True, blank=True, verbose_name=_("gateway"), on_delete=models.CASCADE)
    is_paid = models.BooleanField(verbose_name=_("is paid status"), default=False)
    payment_log = models.TextField(verbose_name=_('logs'), blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), null=True, blank=True, on_delete=models.SET_NULL)
    authority = models.CharField(max_length=64, verbose_name=_('authority'), blank=True)


    class Meta:
        verbose_name = _("Payments")
        verbose_name_plural = _('Payments')


    def __str__(self):
        return self.invoice_number.hex
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._b_is_paid = self.is_paid


    def get_handler_date(self):
        return dict(
            merchant_id=self.gateway.auth_data, amount=self.amount, detail=self.title, 
            user_email=self.user.email, user_phone_number=getattr(self.user, "phone_number", None), 
            callback="http://127.0.0.1:8000/finance/verify"
        )


    @property
    def bank_page(self):
        handler = self.gateway.get_request_handler()
        if handler is not None:
            data = self.get_handler_data()
            link, authority = handler(**data)
            if authority is not None:
                self.authority = authority
                self.save()
            return link
    
    @property
    def title(self):
        return _("Instant payment")
    

    def status_changed(self):
        return self.is_paid != self._b_is_paid
    

    def verify(self, data):
        handler = self.gateway.get_verify_handler()
        if not self.is_paid and handler is not None:
           self.is_paid, _ = handler(**data)
           self.save()
        return self.is_paid
    
    def get_gateway(self):
        gateway = GateWay.objects.filter(is_enable=True).first()
        return gateway.gateway_code
    
    def save_log(self, data, scope='Request handler', save=True):
        generated_log = "[{}][{}] {}\n".format(timezone.now(), scope, data)
        if self.payment_log != '':
            self.payment_log += generated_log
        else:
            self.payment_log = generated_log
        if save:
            self.save()


