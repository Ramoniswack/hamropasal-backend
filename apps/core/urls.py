from django.urls import path
from .views import ShippingSettingsView

urlpatterns = [
    path('settings/shipping/', ShippingSettingsView.as_view(), name='shipping-settings'),
]
