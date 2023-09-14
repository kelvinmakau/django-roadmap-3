# custom_auth/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.user_profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('login_required_message', views.login_required_message, name='login_required_message'),
]