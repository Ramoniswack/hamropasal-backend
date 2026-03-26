from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import HeroBanner, MarketplaceBanner, PromoBanner, ScrollingBanner
from .serializers import (
    HeroBannerSerializer, MarketplaceBannerSerializer,
    PromoBannerSerializer, ScrollingBannerSerializer
)


class HeroBannerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for hero banners
    GET /api/banners/hero/ - List all active hero banners
    """
    queryset = HeroBanner.objects.filter(is_active=True).order_by('order')
    serializer_class = HeroBannerSerializer
    permission_classes = [AllowAny]


class MarketplaceBannerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for marketplace banners
    GET /api/banners/marketplace/ - List all active marketplace banners
    """
    queryset = MarketplaceBanner.objects.filter(is_active=True).order_by('order')
    serializer_class = MarketplaceBannerSerializer
    permission_classes = [AllowAny]


class PromoBannerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for promo banners
    GET /api/banners/promo/ - List all active promo banners
    """
    queryset = PromoBanner.objects.filter(is_active=True)
    serializer_class = PromoBannerSerializer
    permission_classes = [AllowAny]


class ScrollingBannerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for scrolling banners
    GET /api/banners/scrolling/ - List all active scrolling banners
    """
    queryset = ScrollingBanner.objects.filter(is_active=True)
    serializer_class = ScrollingBannerSerializer
    permission_classes = [AllowAny]
