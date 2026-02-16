from django.urls import path
from . import views

urlpatterns = [
    path('redirect/', views.role_based_redirect, name='role_redirect'),
    path('register/', views.register, name='register'),
]
