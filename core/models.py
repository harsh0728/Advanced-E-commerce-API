from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)  # Ensure email is unique
