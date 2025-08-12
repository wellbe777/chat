from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    # is_superuser = models.BooleanField(
    #     default=True
    # )
    # is_staff = models.BooleanField(
    #     default=True
    # )
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []