from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.startup_login, name='startup_login'),
    path('register/', views.startup_register, name='startup_register'),
    path('logout/', views.startup_logout, name='startup_logout'),
    path('dashboard/', views.startup_dashboard, name='startup_dashboard'),
    path('profile/', views.startup_profile, name='startup_profile'),
    path('connection/<int:request_id>/<str:action>/', views.handle_connection_request, name='handle_connection_request'),
    # new endpoints for investor applications
    path('apply/', views.apply_to_investors, name='apply_to_investors'),
    path('apply/<int:investor_id>/', views.apply_to_investors, name='apply_to_investor'),
    path('applications/', views.startup_applications_history, name='startup_applications_history'),
    path('application/<int:application_id>/', views.startup_application_detail, name='startup_application_detail'),
    path('application/<int:application_id>/delete/', views.delete_application, name='delete_application'),
]
