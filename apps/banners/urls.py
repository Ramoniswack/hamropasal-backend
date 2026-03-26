from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HeroBannerViewSet, MarketplaceBannerViewSet,
    PromoBannerViewSet, ScrollingBannerViewSet
)

router = DefaultRouter()
router.register(r'hero', HeroBannerViewSet, basename='hero-banner')
router.register(r'marketplace', MarketplaceBannerViewSet, basename='marketplace-banner')
router.register(r'promo', PromoBannerViewSet, basename='promo-banner')
router.register(r'scrolling', ScrollingBannerViewSet, basename='scrolling-banner')

urlpatterns = [
    path('', include(router.urls)),
]
