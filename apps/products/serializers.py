from rest_framework import serializers
from .models import Product, ProductImage
from apps.categories.serializers import CategoryListSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary']


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product listing"""
    category = CategoryListSerializer(read_only=True)
    primary_image = serializers.SerializerMethodField()
    final_price = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'short_description', 'price', 
            'discount_price', 'final_price', 'discount_percentage',
            'stock', 'category', 'is_featured', 'primary_image'
        ]

    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            return self.context['request'].build_absolute_uri(primary.image.url) if primary.image else None
        first_image = obj.images.first()
        return self.context['request'].build_absolute_uri(first_image.image.url) if first_image and first_image.image else None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single product view"""
    category = CategoryListSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    final_price = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()
    is_in_stock = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'price', 'discount_price', 'final_price', 'discount_percentage',
            'stock', 'is_in_stock', 'category', 'is_featured', 'is_active',
            'images', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
