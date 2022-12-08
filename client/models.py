from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    REQUIRED_FIELDS = ['phone']
    phone = models.CharField(max_length=13, null=True)
    company_name = models.CharField(max_length=256, null=True)

    def save(self):
        self.username = self.phone
        return super().save()
