from celery import shared_task
from finance.models import Payment
from django.db.models import Sum


@shared_task(name='get and send totla purchase')
def get_and_send_total_purchase():
    totla_payment = Payment.objects.filter(is_paid=True).aggregate(total=Sum('amount'))
    print(f"Total Paymen {totla_payment.get('total', 0)}")