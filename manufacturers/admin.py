from django.contrib import admin
from .models import ManufacturerProfile, ConnectionRequest


@admin.register(ManufacturerProfile)
class ManufacturerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'industry', 'location', 'production_capacity')
    search_fields = ('user__username', 'company_name', 'industry', 'location')
    list_filter = ('industry',)


@admin.register(ConnectionRequest)
class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'startup', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('manufacturer__user__username', 'startup__name')
