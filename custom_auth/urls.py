# custom_auth/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.user_profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('coming-soon/', views.coming_soon, name='soon'),
    path('update_profile/', views.update_profile, name='update_profile' ),
    path('view_users/', views.view_users, name='view_users'),
    path('edit_user/<int:user_id>/', views.edit_user,name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
]
