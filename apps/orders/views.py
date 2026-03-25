from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Cart, CartItem, Order
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    CheckoutSerializer
)
from apps.products.models import Product


class CartViewSet(viewsets.ViewSet):
    """API endpoint for shopping cart"""
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """Get current user's cart"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add(self, request):
        """Add item to cart"""
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        if not product_id:
            return Response(
                {'error': 'product_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found or inactive'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check stock
        if product.stock < quantity:
            return Response(
                {'error': f'Only {product.stock} units available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get or create cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Get or create cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Update quantity if item already exists
            new_quantity = cart_item.quantity + quantity
            if product.stock < new_quantity:
                return Response(
                    {'error': f'Only {product.stock} units available'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity = new_quantity
            cart_item.save()
        
        serializer = CartSerializer(cart)
        return Response(
            {
                'message': 'Product added to cart',
                'cart': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['put'])
    def update_item(self, request):
        """Update cart item quantity"""
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')
        
        if not item_id or quantity is None:
            return Response(
                {'error': 'item_id and quantity are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response(
                {'error': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Validate quantity
        if quantity < 1:
            return Response(
                {'error': 'Quantity must be at least 1'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if cart_item.product.stock < quantity:
            return Response(
                {'error': f'Only {cart_item.product.stock} units available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart_item.quantity = quantity
        cart_item.save()
        
        serializer = CartSerializer(cart)
        return Response(
            {
                'message': 'Cart updated',
                'cart': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['delete'])
    def remove_item(self, request):
        """Remove item from cart"""
        item_id = request.data.get('item_id')
        
        if not item_id:
            return Response(
                {'error': 'item_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.delete()
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response(
                {'error': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = CartSerializer(cart)
        return Response(
            {
                'message': 'Item removed from cart',
                'cart': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """Clear all items from cart"""
        try:
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
        except Cart.DoesNotExist:
            pass
        
        return Response(
            {'message': 'Cart cleared'},
            status=status.HTTP_200_OK
        )


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for orders"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            'items', 'items__product', 'status_history'
        )
    
    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """Create order from cart"""
        serializer = CheckoutSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            order_serializer = OrderSerializer(order)
            return Response(
                {
                    'message': 'Order created successfully',
                    'order': order_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def track(self, request, pk=None):
        """Track order status"""
        order = self.get_object()
        return Response({
            'order_number': order.order_number,
            'status': order.status,
            'payment_status': order.payment_status,
            'created_at': order.created_at,
            'confirmed_at': order.confirmed_at,
            'shipped_at': order.shipped_at,
            'delivered_at': order.delivered_at,
            'status_history': [
                {
                    'status': history.status,
                    'notes': history.notes,
                    'created_at': history.created_at
                }
                for history in order.status_history.all()
            ]
        })

