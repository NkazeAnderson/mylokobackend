from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

from django.db import models

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(unique=True, max_length=10)
    isVerified = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField()
    profile_picture = models.FileField(upload_to="profilePics", blank= True, null=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone}"

