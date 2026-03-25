from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    # Cart endpoints
    path('cart/', CartViewSet.as_view({'get': 'list'}), name='cart-list'),
    path('cart/add/', CartViewSet.as_view({'post': 'add'}), name='cart-add'),
    path('cart/update/', CartViewSet.as_view({'put': 'update_item'}), name='cart-update'),
    path('cart/remove/', CartViewSet.as_view({'delete': 'remove_item'}), name='cart-remove'),
    path('cart/clear/', CartViewSet.as_view({'delete': 'clear'}), name='cart-clear'),
    
    # Orders endpoints
    path('', include(router.urls)),
]
