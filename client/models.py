from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import PhoneValidator

class User(AbstractUser):
    REQUIRED_FIELDS = ['phone']
    phone = models.CharField(max_length=13, unique=True, null=True, validators=[PhoneValidator()])
    company_name = models.CharField(max_length=256, null=True)
