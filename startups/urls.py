from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.startup_login, name='startup_login'),
    path('register/', views.startup_register, name='startup_register'),
    path('logout/', views.startup_logout, name='startup_logout'),
    path('dashboard/', views.startup_dashboard, name='startup_dashboard'),
    path('profile/', views.startup_profile, name='startup_profile'),
    path('connection/<int:request_id>/<str:action>/', views.handle_connection_request, name='handle_connection_request'),
    path('apply/<int:investor_id>/', views.apply_to_investor, name='apply_to_investor'),
]
