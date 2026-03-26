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
