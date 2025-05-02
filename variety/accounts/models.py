from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    
    phone_number = PhoneNumberField(blank=False, unique=True)  #format: +919876543210

    def __str__(self):
        return self.username
