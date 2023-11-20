from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    api_key = models.CharField(max_length=255)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    api_key = forms.CharField(max_length=255)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('api_key',)
