from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:investor_id>/', views.apply_to_investor, name='apply_to_investor'),
]
