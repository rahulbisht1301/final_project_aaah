from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('startups/', include('startups.urls')),
    path('investors/', include('investors.urls')),
    path('manufacturers/', include('manufacturers.urls')),
]
