from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import CustomUserCreationForm
from django.contrib.auth import get_user_model

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("Form is valid and user is saved.")  # デバッグメッセージ

            # データベースからユーザーを取得して確認
            User = get_user_model()
            saved_user = User.objects.get(username=user.username)
            if saved_user is not None:
                print(f"User {saved_user.username} is successfully saved in the database.")
            else:
                print("User is not saved in the database.")

            return redirect('login')
        else:
            print("Form is not valid.")  # デバッグメッセージ
            print(form.errors)  # フォームのエラー内容を表示
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

import logging

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            logger.info(f"User {user.username} is successfully authenticated.")  # ログメッセージ
            login(request, user)
            return JsonResponse({'authenticated': True, 'redirect_url': reverse('home')})
        else:
            logger.error("Authentication failed.")  # ログメッセージ
            # Return an 'invalid login' error message.
            return JsonResponse({'authenticated': False})
    else:
        # テスト用の無効なユーザー名とパスワード
        test_username = "invalid_username"
        test_password = "invalid_password"
        test_user = authenticate(request, username=test_username, password=test_password)
        if test_user is None:
            logger.info("Test authentication failed as expected.")  # ログメッセージ
        else:
            logger.error("Test authentication succeeded unexpectedly.")  # ログメッセージ
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    return render(request, 'home.html')
