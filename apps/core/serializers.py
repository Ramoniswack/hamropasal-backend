from rest_framework import serializers
from .models import SiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):
    """Serializer for site settings"""
    
    class Meta:
        model = SiteSettings
        fields = ['shipping_cost', 'free_shipping_threshold', 'tax_rate', 'currency_symbol']
        read_only_fields = ['shipping_cost', 'free_shipping_threshold', 'tax_rate', 'currency_symbol']
