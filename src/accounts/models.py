from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models.signals import post_save


class User(AbstractUser):
    email = models.EmailField(unique=True,max_length=100)
    is_business = models.BooleanField(default=False)
    is_investor = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['username',]
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username

