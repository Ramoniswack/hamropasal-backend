from rest_framework import serializers
from .models import Product, ProductImage, ProductReview
from apps.categories.serializers import CategoryListSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product listing"""
    category = CategoryListSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    rating_average = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    final_price = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'short_description', 'price', 
            'discount_price', 'final_price', 'discount_percentage',
            'stock', 'category', 'is_featured', 'images',
            'rating_average', 'review_count', 'created_at'
        ]
    
    def get_rating_average(self, obj):
        reviews = obj.reviews.filter(is_approved=True)
        if reviews.exists():
            from django.db.models import Avg
            return reviews.aggregate(Avg('rating'))['rating__avg']
        return 0
    
    def get_review_count(self, obj):
        return obj.reviews.filter(is_approved=True).count()


class ProductDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single product view"""
    category = CategoryListSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    rating_average = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    final_price = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()
    is_in_stock = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'price', 'discount_price', 'final_price', 'discount_percentage',
            'stock', 'is_in_stock', 'category', 'is_featured', 'is_active',
            'images', 'rating_average', 'review_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
    
    def get_rating_average(self, obj):
        reviews = obj.reviews.filter(is_approved=True)
        if reviews.exists():
            from django.db.models import Avg
            return reviews.aggregate(Avg('rating'))['rating__avg']
        return 0
    
    def get_review_count(self, obj):
        return obj.reviews.filter(is_approved=True).count()


class ProductReviewSerializer(serializers.ModelSerializer):
    """Serializer for product reviews"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_full_name = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductReview
        fields = [
            'id', 'product', 'user', 'user_name', 'user_full_name',
            'rating', 'title', 'comment', 'is_verified_purchase',
            'is_approved', 'helpful_count', 'can_edit',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'is_verified_purchase', 'is_approved', 'helpful_count', 'created_at', 'updated_at']
    
    def get_user_full_name(self, obj):
        if obj.user.first_name and obj.user.last_name:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return obj.user.username
    
    def get_can_edit(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user == request.user
        return False
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
    
    def validate(self, data):
        request = self.context.get('request')
        product = data.get('product') or self.instance.product
        
        # Check if user has already reviewed this product (only for create)
        if not self.instance:
            from .models import ProductReview
            if ProductReview.objects.filter(user=request.user, product=product).exists():
                raise serializers.ValidationError("You have already reviewed this product")
        
        # Check if user has purchased and received this product
        from apps.orders.models import Order, OrderItem
        has_purchased = OrderItem.objects.filter(
            order__user=request.user,
            order__status='delivered',
            product=product
        ).exists()
        
        if not has_purchased:
            raise serializers.ValidationError(
                "You can only review products you have purchased and received"
            )
        
        return data
    
    def create(self, validated_data):
        # Set user from request
        validated_data['user'] = self.context['request'].user
        
        # Set verified purchase flag
        validated_data['is_verified_purchase'] = True
        
        return super().create(validated_data)
