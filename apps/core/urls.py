from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShippingSettingsView, NewsletterViewSet

router = DefaultRouter()
router.register(r'newsletter', NewsletterViewSet, basename='newsletter')

urlpatterns = [
    path('settings/shipping/', ShippingSettingsView.as_view(), name='shipping-settings'),
    path('', include(router.urls)),
]
