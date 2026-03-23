from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'parent', 'is_active', 'created_at', 'subcategories']
        read_only_fields = ['slug', 'created_at']

    def get_subcategories(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.filter(is_active=True), many=True).data
        return []


class CategoryListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing categories"""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'parent']
