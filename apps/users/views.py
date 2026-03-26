from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import Wishlist
from .serializers import (
    UserRegistrationSerializer, 
    UserSerializer, 
    UserProfileUpdateSerializer,
    ChangePasswordSerializer,
    WishlistSerializer,
    BillingAddressSerializer
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """User login endpoint - accepts email or username"""
    
    def post(self, request, *args, **kwargs):
        # Check if user is trying to login with email
        username_or_email = request.data.get('username', '')
        password = request.data.get('password', '')
        
        # Try to find user by email if @ is in the username field
        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                # Create new data dict with actual username
                data = request.data.copy()
                data['username'] = user.username
                request._full_data = data
            except User.DoesNotExist:
                return Response(
                    {'detail': 'Invalid email or password'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        # Call parent class to handle JWT token generation
        try:
            return super().post(request, *args, **kwargs)
        except Exception:
            return Response(
                {'detail': 'Invalid email or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    """User logout endpoint - blacklists refresh token"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(
                {'message': 'Logout successful'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update current user profile"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UserProfileUpdateSerializer
        return UserSerializer


class ChangePasswordView(APIView):
    """Change user password"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response(
                {'message': 'Password changed successfully'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WishlistViewSet(viewsets.ModelViewSet):
    """API endpoint for wishlist"""
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('product')
    
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
            from apps.products.models import Product
            if not Product.objects.filter(id=product_id, is_active=True).exists():
                return Response(
                    {'error': 'Product not found or inactive'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            Wishlist.objects.create(user=request.user, product_id=product_id)
            return Response(
                {'message': 'Product added to wishlist', 'in_wishlist': True},
                status=status.HTTP_201_CREATED
            )



class BillingAddressView(generics.RetrieveUpdateAPIView):
    """Get and update billing address"""
    serializer_class = BillingAddressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
