from django.dispatch import receiver
from django.db.models.signals import post_save, post_init
from finance.models import Payment


@receiver(post_save, sender=Payment)
def callback(sender, instance, created, **kwargs):
    print("signal called!!!")
    if instance.is_paid and not instance._b_is_paid:
        print("Pruchase signal fierd!!!")
        purchase = instance.purchases.first()
        purchase.status = purchase.PAID
        purchase.save()


@receiver(post_init, sender=Payment)
def store_is_paid_status(sender, instance, **kwargs):
    print("post init signal called!!!")
    instance._b_is_paid = instance.is_paid



    