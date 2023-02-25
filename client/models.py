from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import PhoneValidator

class User(AbstractUser):
    REQUIRED_FIELDS = ['phone']
    phone = models.CharField(max_length=13, unique=True, null=True)#, validators=[PhoneValidator()])
    company_name = models.CharField(max_length=256, null=True)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.old_password = self.password


    def save(self, *args, **kwargs):
        if self._state.adding or (self.password != self.old_password):
            super().set_password(self.password)
        super().save(*args, **kwargs)