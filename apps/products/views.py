from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer


class ProductListView(generics.ListAPIView):
    """List all active products with filtering and search"""
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured', 'is_active']
    search_fields = ['name', 'description', 'short_description']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']


class ProductDetailView(generics.RetrieveAPIView):
    """Retrieve a single product with all details"""
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'


class FeaturedProductListView(generics.ListAPIView):
    """List featured products"""
    queryset = Product.objects.filter(is_active=True, is_featured=True).select_related('category').prefetch_related('images')
    serializer_class = ProductListSerializer
    ordering = ['-created_at']
