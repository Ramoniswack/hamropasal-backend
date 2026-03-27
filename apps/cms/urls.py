from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SiteSettingsViewSet, NavigationMenuViewSet, MegaMenuSettingsViewSet, MegaMenuCategoryViewSet, FooterColumnViewSet,
    StoreViewSet, TestimonialViewSet, FAQViewSet, FeatureViewSet,
    VendorViewSet, AboutHeroViewSet, AboutSectionViewSet,
    AboutImageViewSet, ContactSubmissionViewSet,
    PageViewSet, WidgetViewSet
)

router = DefaultRouter()
router.register(r'site-settings', SiteSettingsViewSet, basename='site-settings')
router.register(r'navigation', NavigationMenuViewSet, basename='navigation')
router.register(r'megamenu-settings', MegaMenuSettingsViewSet, basename='megamenu-settings')
router.register(r'megamenu-categories', MegaMenuCategoryViewSet, basename='megamenu-categories')
router.register(r'footer', FooterColumnViewSet, basename='footer')
router.register(r'stores', StoreViewSet, basename='stores')
router.register(r'testimonials', TestimonialViewSet, basename='testimonials')
router.register(r'faqs', FAQViewSet, basename='faqs')
router.register(r'features', FeatureViewSet, basename='features')
router.register(r'vendors', VendorViewSet, basename='vendors')
router.register(r'about-hero', AboutHeroViewSet, basename='about-hero')
router.register(r'about-sections', AboutSectionViewSet, basename='about-sections')
router.register(r'about-images', AboutImageViewSet, basename='about-images')
router.register(r'contact', ContactSubmissionViewSet, basename='contact')
router.register(r'pages', PageViewSet, basename='pages')
router.register(r'widgets', WidgetViewSet, basename='widgets')

urlpatterns = [
    path('', include(router.urls)),
]
