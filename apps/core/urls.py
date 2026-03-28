from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShippingSettingsView, NewsletterViewSet, analytics_dashboard, analytics_api

router = DefaultRouter()
router.register(r'newsletter', NewsletterViewSet, basename='newsletter')

urlpatterns = [
    path('settings/shipping/', ShippingSettingsView.as_view(), name='shipping-settings'),
    path('analytics/dashboard/', analytics_dashboard, name='analytics-dashboard'),
    path('analytics/api/', analytics_api, name='analytics-api'),
    path('', include(router.urls)),
]
