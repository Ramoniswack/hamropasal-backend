from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Sum, Count, Avg, F, Q
from django.utils.html import format_html
from django.views.decorators.cache import never_cache
from apps.products.models import Product, ProductReview
from apps.orders.models import Order, OrderItem
from apps.users.models import Wishlist
from apps.orders.models import Cart, CartItem
from django.db import models


@never_cache
def analytics_dashboard_view(request):
    """Analytics Dashboard View"""
    # Revenue Analytics
    total_revenue = Order.objects.filter(
        status='delivered'
    ).aggregate(total=Sum('total'))['total'] or 0
    
    total_orders = Order.objects.filter(status='delivered').count()
    pending_orders = Order.objects.filter(status='pending').count()
    
    # Most Sold Products
    most_sold_products = Product.objects.annotate(
        total_sold=Sum('order_items__quantity', filter=models.Q(order_items__order__status='delivered'))
    ).order_by('-total_sold')[:10]
    
    # Most Wishlisted Products
    most_wishlisted = Product.objects.annotate(
        wishlist_count=Count('wishlist')
    ).order_by('-wishlist_count')[:10]
    
    # Most Added to Cart Products
    most_in_cart = Product.objects.annotate(
        cart_count=Count('cart_items')
    ).order_by('-cart_count')[:10]
    
    # Recent Reviews
    recent_reviews = ProductReview.objects.select_related(
        'product', 'user'
    ).order_by('-created_at')[:10]
    
    # Average Rating by Product
    top_rated_products = Product.objects.annotate(
        avg_rating=Avg('reviews__rating', filter=models.Q(reviews__is_approved=True)),
        total_reviews=Count('reviews', filter=models.Q(reviews__is_approved=True))
    ).filter(total_reviews__gt=0).order_by('-avg_rating')[:10]
    
    # Low Stock Products
    low_stock_products = Product.objects.filter(
        is_active=True,
        stock__lte=F('low_stock_threshold')
    ).order_by('stock')[:10]
    
    # Order Status Distribution
    order_status_stats = Order.objects.values('status').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'site_header': 'Hamro Pasal Administration',
        'site_title': 'Analytics Dashboard',
        'title': 'Analytics Dashboard',
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'most_sold_products': most_sold_products,
        'most_wishlisted': most_wishlisted,
        'most_in_cart': most_in_cart,
        'recent_reviews': recent_reviews,
        'top_rated_products': top_rated_products,
        'low_stock_products': low_stock_products,
        'order_status_stats': order_status_stats,
        'has_permission': True,
    }
    
    return render(request, 'admin/analytics_dashboard.html', context)


# Create a proxy model to show Analytics in the admin sidebar
class AnalyticsProxy(models.Model):
    """Proxy model to add Analytics Dashboard link to admin sidebar"""
    class Meta:
        managed = False
        verbose_name = "Analytics Dashboard"
        verbose_name_plural = "📊 Analytics Dashboard"
        app_label = 'core'


@admin.register(AnalyticsProxy)
class AnalyticsProxyAdmin(admin.ModelAdmin):
    """Admin for Analytics Proxy - redirects to analytics dashboard"""
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def changelist_view(self, request, extra_context=None):
        """Redirect to analytics dashboard"""
        return analytics_dashboard_view(request)
