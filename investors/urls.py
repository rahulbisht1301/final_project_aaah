from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.investor_login, name='investor_login'),
    path('register/', views.investor_register, name='investor_register'),
    path('logout/', views.investor_logout, name='investor_logout'),
    path('dashboard/', views.investor_dashboard, name='investor_dashboard'),
    path('profile/', views.investor_profile, name='investor_profile'),
    path('browse/', views.browse_startups, name='browse_startups'),
    path('startup/<int:startup_id>/', views.startup_detail_investor, name='startup_detail_investor'),
    path('applications/', views.investor_applications, name='investor_applications'),
    path('application/<int:application_id>/<str:status>/', views.update_application_status, name='update_application_status'),
]
