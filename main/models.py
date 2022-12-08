from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=256, null=True)
    ceo = models.ForeignKey('client.User', on_delete=models.SET_NULL, null=True, related_name='company_ceo')
    staffs = models.ManyToManyField('client.User', related_name="company")
    