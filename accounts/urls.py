from django.urls import path
from . import views

urlpatterns = [
    path('redirect/', views.role_based_redirect, name='role_redirect'),
    path('register/', views.register, name='register'),
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent_messages, name='sent_messages'),
    path('message/<int:message_id>/', views.view_message, name='view_message'),
    path('compose/', views.compose_message, name='compose_message'),
    path('compose/<int:recipient_id>/', views.compose_message, name='compose_message_to'),
]
