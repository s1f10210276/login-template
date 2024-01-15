from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    api_key = models.CharField(max_length=255)
