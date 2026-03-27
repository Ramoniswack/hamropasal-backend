from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SiteSettings
from .serializers import SiteSettingsSerializer


class ShippingSettingsView(APIView):
    """
    API endpoint to get shipping settings
    """
    permission_classes = []  # Public endpoint
    
    def get(self, request):
        """Get current shipping settings"""
        settings = SiteSettings.load()
        serializer = SiteSettingsSerializer(settings)
        return Response(serializer.data, status=status.HTTP_200_OK)



from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from .models import NewsletterSubscriber
from .serializers_extended import NewsletterSubscriberSerializer


class NewsletterViewSet(viewsets.GenericViewSet):
    """Newsletter subscription management"""
    serializer_class = NewsletterSubscriberSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def subscribe(self, request):
        """Subscribe to newsletter"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Successfully subscribed to newsletter! Check your email for confirmation."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def unsubscribe(self, request):
        """Unsubscribe from newsletter"""
        email = request.data.get('email')
        token = request.data.get('token')
        
        if not email or not token:
            return Response(
                {"detail": "Email and token are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            subscriber = NewsletterSubscriber.objects.get(
                email=email,
                unsubscribe_token=token
            )
            subscriber.is_active = False
            subscriber.unsubscribed_at = timezone.now()
            subscriber.save()
            return Response({"detail": "Successfully unsubscribed from newsletter"})
        except NewsletterSubscriber.DoesNotExist:
            return Response(
                {"detail": "Invalid email or token"},
                status=status.HTTP_404_NOT_FOUND
            )
