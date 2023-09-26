from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('send_message/', views.send_message, name='send_message'),
]
