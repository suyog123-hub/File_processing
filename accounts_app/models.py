from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    address= models.CharField(max_length=255,null=True)
    phone_number = models.CharField(max_length=20,null=True)
    date_joined=models.DateTimeField(auto_now=True,null=True)

    