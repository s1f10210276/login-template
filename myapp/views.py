from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str  # use force_str instead of force_text
from .forms import CustomUserCreationForm
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User

import secrets

User = get_user_model()
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # ユーザー名が@iniad.orgで終わることを確認
            username = form.cleaned_data.get('username')
            if not username.endswith('@iniad.org'):
                form.add_error('username', 'ユーザーネームは@iniad.orgで終わる必要があります')
                return render(request, 'register.html', {'form': form})

           
            password = form.cleaned_data.get('password1')
            user = form.save(commit=False)
            user.set_password(password)
            user.is_active = False  # ユーザーを非アクティブに設定
            user.save()

            # メール確認のためのトークンを生成
            token = default_token_generator.make_token(user)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
            msg = EmailMultiAlternatives(mail_subject, message, 's1f102100197@iniad.org', [username])
            msg.attach_alternative(message, "text/html")
            msg.send()

            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)  # Use User here
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            return HttpResponse('Activation link is invalid!')
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        return HttpResponse('Activation link is invalid!')


import logging

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                logger.info(f"User {user.username} is successfully authenticated.")  # ログメッセージ
                return JsonResponse({'authenticated': True, 'redirect_url': reverse('home')})
            else:
                return HttpResponse('Your account is not active, please check your email.')
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

