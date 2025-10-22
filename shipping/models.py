from django.db import models
from django.contrib.auth.models import User



class ShippingAddres(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addreses")
    city = models.CharField(max_length=62, blank=True)
    zip_code = models.CharField(max_length=16)
    addres = models.TextField()
    number = models.PositiveSmallIntegerField()

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.user)