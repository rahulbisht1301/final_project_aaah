from django.urls import path
from . import views

urlpatterns = [
    path('applications/', views.investor_applications, name='investor_applications'),
    path('application/<int:application_id>/<str:status>/', views.update_application_status, name='update_application_status'),
]
