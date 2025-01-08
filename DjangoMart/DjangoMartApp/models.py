from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=50, null=False)
    middle_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    phone_number = models.CharField(max_length=15, null=False)
    represented_company_name = models.CharField(max_length=100, null=False)
    verified_representative = models.BooleanField(default=False)
    purchased_machines = models.IntegerField(default=0)

