from django.urls import path
from .views import ProductListView, ProductDetailView, FeaturedProductListView, ProductReviewViewSet

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('featured/', FeaturedProductListView.as_view(), name='featured-products'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('<slug:product_slug>/reviews/', ProductReviewViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='product-reviews'),
    path('<slug:product_slug>/reviews/<int:pk>/', ProductReviewViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='product-review-detail'),
]
