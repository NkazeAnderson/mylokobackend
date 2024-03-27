from django.contrib import admin
from .models import Payments, CustomPayments

# Register your models here.
admin.site.register(Payments)
admin.site.register(CustomPayments)