from rest_framework import serializers
from .models import HeroBanner, MarketplaceBanner, PromoBanner, ScrollingBanner


class HeroBannerSerializer(serializers.ModelSerializer):
    """Serializer for hero banners"""
    class Meta:
        model = HeroBanner
        fields = [
            'id', 'title', 'description', 'image', 'discount_percentage',
            'discount_text', 'price', 'price_text', 'button_text',
            'button_link', 'order', 'is_active', 'created_at'
        ]


class MarketplaceBannerSerializer(serializers.ModelSerializer):
    """Serializer for marketplace banners"""
    class Meta:
        model = MarketplaceBanner
        fields = [
            'id', 'title', 'description', 'image', 'button_text',
            'button_link', 'order', 'is_active', 'created_at'
        ]


class PromoBannerSerializer(serializers.ModelSerializer):
    """Serializer for promo banners"""
    class Meta:
        model = PromoBanner
        fields = [
            'id', 'title', 'description', 'image', 'button_text',
            'button_link', 'is_active', 'created_at'
        ]


class ScrollingBannerSerializer(serializers.ModelSerializer):
    """Serializer for scrolling banners"""
    class Meta:
        model = ScrollingBanner
        fields = ['id', 'text', 'is_active', 'created_at']
