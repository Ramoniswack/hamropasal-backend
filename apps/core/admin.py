from django.contrib import admin
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['shipping_cost', 'free_shipping_threshold', 'currency_symbol', 'updated_at']
    
    fieldsets = (
        ('Shipping Settings', {
            'fields': ('shipping_cost', 'free_shipping_threshold')
        }),
        ('Tax Settings', {
            'fields': ('tax_rate',)
        }),
        ('Currency', {
            'fields': ('currency_symbol',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False
