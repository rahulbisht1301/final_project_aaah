from django.contrib import admin
from .models import InvestorProfile, FavoriteStartup


@admin.register(InvestorProfile)
class InvestorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'investment_range_min', 'investment_range_max', 'industry_focus', 'location')
    search_fields = ('user__username', 'industry_focus', 'location')
    readonly_fields = ('user',)


@admin.register(FavoriteStartup)
class FavoriteStartupAdmin(admin.ModelAdmin):
    list_display = ('user', 'startup', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'startup__name')
    readonly_fields = ('created_at',)
