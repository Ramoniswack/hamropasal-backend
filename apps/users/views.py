from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from .models import Wishlist
from .serializers import UserRegistrationSerializer, UserSerializer, WishlistSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint for users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class WishlistViewSet(viewsets.ModelViewSet):
    """API endpoint for wishlist"""
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def toggle(self, request):
        """Toggle product in wishlist"""
        product_id = request.data.get('product_id')
        if not product_id:
            return Response(
                {'error': 'product_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        wishlist_item = Wishlist.objects.filter(
            user=request.user,
            product_id=product_id
        ).first()
        
        if wishlist_item:
            wishlist_item.delete()
            return Response(
                {'message': 'Product removed from wishlist', 'in_wishlist': False},
                status=status.HTTP_200_OK
            )
        else:
            Wishlist.objects.create(user=request.user, product_id=product_id)
            return Response(
                {'message': 'Product added to wishlist', 'in_wishlist': True},
                status=status.HTTP_201_CREATED
            )
