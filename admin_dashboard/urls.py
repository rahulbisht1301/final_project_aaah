from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('startups/', views.manage_startups, name='manage_startups'),
    path('startup/<int:startup_id>/<str:action>/', views.startup_approval, name='startup_approval'),
    path('users/', views.manage_users, name='manage_users'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('applications/', views.manage_applications, name='manage_applications'),
    path('connections/', views.manage_connections, name='manage_connections'),
]
