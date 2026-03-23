from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import (
    SiteSettings, NavigationMenu, FooterColumn, Store,
    Testimonial, FAQ, Feature, Vendor,
    AboutHero, AboutSection, AboutImage, ContactSubmission,
    Page, Widget
)
from .serializers import (
    SiteSettingsSerializer, NavigationMenuSerializer, FooterColumnSerializer,
    StoreSerializer, TestimonialSerializer, FAQSerializer, FeatureSerializer,
    VendorSerializer, AboutHeroSerializer, AboutSectionSerializer,
    AboutImageSerializer, ContactSubmissionSerializer
)


class SiteSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for site settings"""
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current site settings"""
        settings = SiteSettings.objects.first()
        if settings:
            serializer = self.get_serializer(settings)
            return Response(serializer.data)
        return Response({'error': 'Site settings not found'}, status=status.HTTP_404_NOT_FOUND)


class NavigationMenuViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for navigation menu"""
    queryset = NavigationMenu.objects.filter(is_active=True, parent=None).order_by('order')
    serializer_class = NavigationMenuSerializer
    permission_classes = [AllowAny]


class FooterColumnViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for footer columns"""
    queryset = FooterColumn.objects.filter(is_active=True).order_by('order')
    serializer_class = FooterColumnSerializer
    permission_classes = [AllowAny]


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for store locations"""
    queryset = Store.objects.filter(is_active=True).order_by('order')
    serializer_class = StoreSerializer
    permission_classes = [AllowAny]


class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for testimonials"""
    queryset = Testimonial.objects.filter(is_active=True).order_by('order')
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for FAQs"""
    queryset = FAQ.objects.filter(is_active=True).order_by('order')
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]


class FeatureViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for features"""
    queryset = Feature.objects.filter(is_active=True).order_by('order')
    serializer_class = FeatureSerializer
    permission_classes = [AllowAny]


class VendorViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for vendors"""
    queryset = Vendor.objects.filter(is_active=True)
    serializer_class = VendorSerializer
    permission_classes = [AllowAny]


# About Page ViewSets
class AboutHeroViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for about hero section"""
    queryset = AboutHero.objects.filter(is_active=True)
    serializer_class = AboutHeroSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current about hero"""
        hero = AboutHero.objects.filter(is_active=True).first()
        if hero:
            serializer = self.get_serializer(hero)
            return Response(serializer.data)
        return Response({'error': 'About hero not found'}, status=status.HTTP_404_NOT_FOUND)


class AboutSectionViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for about sections"""
    queryset = AboutSection.objects.filter(is_active=True).order_by('order')
    serializer_class = AboutSectionSerializer
    permission_classes = [AllowAny]


class AboutImageViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for about images"""
    queryset = AboutImage.objects.filter(is_active=True).order_by('order')
    serializer_class = AboutImageSerializer
    permission_classes = [AllowAny]


# Contact Form ViewSet
class ContactSubmissionViewSet(viewsets.ModelViewSet):
    """API endpoint for contact form submissions"""
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']  # Only allow POST requests
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'message': 'Thank you! Your message has been sent successfully.'},
            status=status.HTTP_201_CREATED
        )



# Widget-Based Page Builder ViewSets
class PageViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for dynamic pages"""
    queryset = Page.objects.filter(is_active=True)
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            from .serializers import PageListSerializer
            return PageListSerializer
        from .serializers import PageSerializer
        return PageSerializer


class WidgetViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for widgets"""
    queryset = Widget.objects.filter(is_active=True)
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        from .serializers import WidgetDetailSerializer
        return WidgetDetailSerializer
