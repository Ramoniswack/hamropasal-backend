from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.db import models
from django.db.models import Sum, Count, Avg, Q, F
from .models import SiteSettings, AnalyticsProxy, NewsletterSubscriber


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['shipping_cost', 'free_shipping_threshold', 'currency_symbol', 'updated_at']
    
    fieldsets = (
        ('Shipping Settings', {
            'fields': ('shipping_cost', 'free_shipping_threshold'),
            'description': 'Configure shipping costs and free shipping threshold'
        }),
        ('Tax Settings', {
            'fields': ('tax_rate',),
            'description': 'Set tax rate percentage'
        }),
        ('Currency', {
            'fields': ('currency_symbol',),
            'description': 'Currency symbol for display'
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


@admin.register(AnalyticsProxy)
class AnalyticsProxyAdmin(admin.ModelAdmin):
    """Analytics Dashboard accessible from admin sidebar"""
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_module_permission(self, request):
        return request.user.is_staff
    
    def changelist_view(self, request, extra_context=None):
        """Redirect to new analytics dashboard"""
        from django.shortcuts import redirect
        return redirect('/admin/analyticsDashboard/')


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'name']
    readonly_fields = ['subscribed_at', 'unsubscribed_at', 'unsubscribe_token']
    date_hierarchy = 'subscribed_at'
    actions = ['activate_subscribers', 'deactivate_subscribers']
    
    def activate_subscribers(self, request, queryset):
        queryset.update(is_active=True, unsubscribed_at=None)
        self.message_user(request, f"{queryset.count()} subscribers activated.")
    activate_subscribers.short_description = "Activate selected subscribers"
    
    def deactivate_subscribers(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_active=False, unsubscribed_at=timezone.now())
        self.message_user(request, f"{queryset.count()} subscribers deactivated.")
    deactivate_subscribers.short_description = "Deactivate selected subscribers"
