from django.db import models
from Properties.models import Property
from Users.models import CustomUser

# Create your models here.
class Payments(models.Model):
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True)
    paid_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=15, choices=[("Processing", "processing"),("Paid", "paid"),("Failed", "failed"),], default="processing")
    is_verified = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    
class CustomPayments(models.Model):
    name = models.CharField(max_length=20)
    paid_by = models.ForeignKey(CustomUser,  on_delete=models.SET_NULL, null=True)
    issued_by = models.ForeignKey(CustomUser,  on_delete=models.SET_NULL, null=True, related_name="issuer")
    amount = models.IntegerField()
    status = models.CharField(max_length=15, choices=[("Processing", "processing"),("Paid", "paid"),("Failed", "failed"),], default="processing")
    date = models.DateField(auto_now_add=True)
