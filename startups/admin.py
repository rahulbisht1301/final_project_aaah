from django.contrib import admin
from .models import Startup, InvestmentApplication


@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):
    list_display = ('name', 'founder', 'niche', 'stage', 'valuation', 'approved')
    list_filter = ('approved', 'stage', 'niche')
    search_fields = ('name', 'founder__username', 'niche')
    readonly_fields = ('founder',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('founder', 'name', 'niche', 'stage')
        }),
        ('Financial Info', {
            'fields': ('valuation',)
        }),
        ('Details', {
            'fields': ('vision', 'pitch_deck', 'demo_video')
        }),
        ('Contact Info', {
            'fields': ('email', 'phone', 'website')
        }),
        ('Status', {
            'fields': ('approved',)
        }),
    )


@admin.register(InvestmentApplication)
class InvestmentApplicationAdmin(admin.ModelAdmin):
    list_display = ('startup', 'investor', 'amount_requested', 'equity_offered', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('startup__name', 'investor__user__username')
    readonly_fields = ('created_at',)
