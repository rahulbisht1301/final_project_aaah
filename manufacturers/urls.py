from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.manufacturer_login, name='manufacturer_login'),
    path('register/', views.manufacturer_register, name='manufacturer_register'),
    path('logout/', views.manufacturer_logout, name='manufacturer_logout'),
    path('dashboard/', views.manufacturer_dashboard, name='manufacturer_dashboard'),
    path('profile/', views.manufacturer_profile, name='manufacturer_profile'),
    path('connections/', views.connection_history, name='connection_history'),
    path('startups/', views.startup_list, name='startup_list'),
    path('startup/<int:startup_id>/', views.startup_detail, name='startup_detail'),
    path('connect/<int:startup_id>/', views.connect_to_startup, name='connect_to_startup'),
]
