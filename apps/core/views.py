"""
Core Views - API and Analytics Dashboard
"""
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.utils import timezone

from .models import SiteSettings, NewsletterSubscriber
from .serializers import SiteSettingsSerializer
from .serializers_extended import NewsletterSubscriberSerializer
from .services import AnalyticsService


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


class NewsletterViewSet(viewsets.GenericViewSet):
    """Newsletter subscription management"""
    serializer_class = NewsletterSubscriberSerializer
    permission_classes = [AllowAny]
    
    def create(self, request):
        """Subscribe to newsletter"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            # Check if already subscribed
            if NewsletterSubscriber.objects.filter(email=email).exists():
                return Response(
                    {'message': 'This email is already subscribed'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save()
            return Response(
                {'message': 'Successfully subscribed to newsletter'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def unsubscribe(self, request):
        """Unsubscribe from newsletter"""
        email = request.data.get('email')
        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            subscriber = NewsletterSubscriber.objects.get(email=email)
            subscriber.is_active = False
            subscriber.save()
            return Response(
                {'message': 'Successfully unsubscribed'},
                status=status.HTTP_200_OK
            )
        except NewsletterSubscriber.DoesNotExist:
            return Response(
                {'error': 'Email not found'},
                status=status.HTTP_404_NOT_FOUND
            )


# Analytics Dashboard Views
@staff_member_required
def analytics_dashboard(request):
    """Render the analytics dashboard"""
    return render(request, 'admin/analytics_dashboard.html')


@staff_member_required
def analytics_api(request):
    """API endpoint for analytics data"""
    try:
        # Get all analytics data
        kpis = AnalyticsService.get_dashboard_kpis()
        revenue_by_day = AnalyticsService.get_revenue_by_day(days=30)
        orders_by_day = AnalyticsService.get_orders_by_day(days=30)
        revenue_by_category = AnalyticsService.get_revenue_by_category()
        top_products = AnalyticsService.get_top_selling_products(limit=10)
        customer_growth = AnalyticsService.get_customer_growth(months=6)
        order_status = AnalyticsService.get_order_status_distribution()
        low_stock_products = AnalyticsService.get_low_stock_products(limit=10)
        
        return JsonResponse({
            'success': True,
            'data': {
                'kpis': kpis,
                'revenue_by_day': revenue_by_day,
                'orders_by_day': orders_by_day,
                'revenue_by_category': revenue_by_category,
                'top_products': top_products,
                'customer_growth': customer_growth,
                'order_status': order_status,
                'low_stock_products': low_stock_products,
            }
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
