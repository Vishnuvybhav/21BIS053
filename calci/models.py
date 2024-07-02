from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Number(models.Model):
    value = models.IntegerField()

class User(AbstractUser):
    # Add any additional fields here if needed
    pass