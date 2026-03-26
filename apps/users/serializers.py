from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Wishlist
from apps.products.serializers import ProductListSerializer

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'user_type', 'phone', 'address']
        extra_kwargs = {
            'email': {'required': True},
            'user_type': {'required': False},
            'phone': {'required': False},
            'address': {'required': False}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            user_type=validated_data.get('user_type', 'customer'),
            phone=validated_data.get('phone', ''),
            address=validated_data.get('address', '')
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'phone', 'address', 'first_name', 'last_name', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    class Meta:
        model = User
        fields = ['phone', 'address', 'first_name', 'last_name']


class BillingAddressSerializer(serializers.ModelSerializer):
    """Serializer for billing address"""
    class Meta:
        model = User
        fields = [
            'billing_first_name', 'billing_last_name', 'billing_address',
            'billing_apartment', 'billing_city', 'billing_state', 
            'billing_zip_code', 'billing_country', 'billing_phone', 'billing_email'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value


class WishlistSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'product_id', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_product_id(self, value):
        from apps.products.models import Product
        if not Product.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Product not found or inactive")
        return value
