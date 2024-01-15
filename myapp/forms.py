from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    api_key = forms.CharField(max_length=255)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('api_key',)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username.endswith('@iniad.org'):
           raise ValidationError("無効なユーザーネームです。")  # 一般的なエラーメッセージを表示
        return username
