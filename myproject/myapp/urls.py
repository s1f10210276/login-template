from django.urls import path
from . import views  # ここで . は現在のアプリケーションを指します

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'), # login_view はログインビューの名前です
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    # 他のURLパス...
]
