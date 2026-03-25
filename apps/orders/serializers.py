from rest_framework import serializers
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem, OrderStatusHistory
from apps.products.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for cart items"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    product_image = serializers.SerializerMethodField()
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    stock_available = serializers.IntegerField(source='product.stock', read_only=True)
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_name', 'product_slug', 'product_image',
            'quantity', 'unit_price', 'subtotal', 'stock_available', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_product_image(self, obj):
        primary_image = obj.product.images.filter(is_primary=True).first()
        if primary_image:
            return primary_image.image.url if primary_image.image else None
        return None
    
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value
    
    def validate(self, data):
        product = data.get('product') or self.instance.product
        quantity = data.get('quantity', 1)
        
        # Check if product is active
        if not product.is_active:
            raise serializers.ValidationError("This product is no longer available")
        
        # Check stock availability
        if product.stock < quantity:
            raise serializers.ValidationError(
                f"Only {product.stock} units available in stock"
            )
        
        return data


class CartSerializer(serializers.ModelSerializer):
    """Serializer for shopping cart"""
    items = CartItemSerializer(many=True, read_only=True)
    item_count = serializers.IntegerField(read_only=True)
    total_quantity = serializers.IntegerField(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'item_count', 'total_quantity', 'subtotal', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items"""
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_slug', 'product_name', 'product_sku',
            'quantity', 'unit_price', 'discount_price', 'subtotal', 'created_at'
        ]
        read_only_fields = ['id', 'product_name', 'product_sku', 'unit_price', 'discount_price', 'subtotal', 'created_at']


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    """Serializer for order status history"""
    changed_by_username = serializers.CharField(source='changed_by.username', read_only=True)
    
    class Meta:
        model = OrderStatusHistory
        fields = ['id', 'status', 'notes', 'changed_by_username', 'created_at']
        read_only_fields = ['id', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for orders"""
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)
    item_count = serializers.IntegerField(read_only=True)
    total_quantity = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'payment_status',
            'subtotal', 'shipping_cost', 'tax', 'discount', 'total',
            'shipping_address', 'shipping_city', 'shipping_state', 
            'shipping_zip_code', 'shipping_country',
            'customer_name', 'customer_email', 'customer_phone',
            'notes', 'coupon_code',
            'items', 'status_history', 'item_count', 'total_quantity',
            'created_at', 'updated_at', 'confirmed_at', 'shipped_at', 'delivered_at'
        ]
        read_only_fields = [
            'id', 'order_number', 'subtotal', 'total', 'item_count', 'total_quantity',
            'created_at', 'updated_at', 'confirmed_at', 'shipped_at', 'delivered_at'
        ]


class CheckoutSerializer(serializers.Serializer):
    """Serializer for checkout process"""
    shipping_address = serializers.CharField(max_length=500)
    shipping_city = serializers.CharField(max_length=100)
    shipping_state = serializers.CharField(max_length=100)
    shipping_zip_code = serializers.CharField(max_length=20)
    shipping_country = serializers.CharField(max_length=100, default='Nepal')
    customer_name = serializers.CharField(max_length=200)
    customer_email = serializers.EmailField()
    customer_phone = serializers.CharField(max_length=20)
    notes = serializers.CharField(required=False, allow_blank=True)
    coupon_code = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        user = self.context['request'].user
        
        # Check if cart exists and has items
        try:
            cart = Cart.objects.get(user=user)
            if cart.items.count() == 0:
                raise serializers.ValidationError("Cart is empty")
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Cart not found")
        
        # Validate stock for all items
        for item in cart.items.all():
            if not item.product.is_active:
                raise serializers.ValidationError(
                    f"Product '{item.product.name}' is no longer available"
                )
            if item.product.stock < item.quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for '{item.product.name}'. Only {item.product.stock} available"
                )
        
        return data
    
    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.get(user=user)
        
        # Calculate totals
        subtotal = cart.subtotal
        shipping_cost = 100  # Fixed shipping cost (can be dynamic)
        tax = 0  # No tax for now
        discount = 0  # No discount for now
        total = subtotal + shipping_cost + tax - discount
        
        # Create order
        order = Order.objects.create(
            user=user,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax=tax,
            discount=discount,
            total=total,
            **validated_data
        )
        
        # Create order items from cart items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                product_sku=cart_item.product.sku,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.price,
                discount_price=cart_item.product.discount_price,
            )
        
        # Create initial status history
        OrderStatusHistory.objects.create(
            order=order,
            status='pending',
            notes='Order created',
            changed_by=user
        )
        
        # Clear cart
        cart.items.all().delete()
        
        return order
