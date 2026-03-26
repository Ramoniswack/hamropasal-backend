from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.db import models
from django.db.models import Sum, Count, Avg, Q, F
from .models import SiteSettings, AnalyticsProxy


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['shipping_cost', 'free_shipping_threshold', 'currency_symbol', 'updated_at']
    
    fieldsets = (
        ('⚙️ Shipping Settings', {
            'fields': ('shipping_cost', 'free_shipping_threshold'),
            'description': 'Configure shipping costs and free shipping threshold'
        }),
        ('💰 Tax Settings', {
            'fields': ('tax_rate',),
            'description': 'Set tax rate percentage'
        }),
        ('💵 Currency', {
            'fields': ('currency_symbol',),
            'description': 'Currency symbol for display'
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


@admin.register(AnalyticsProxy)
class AnalyticsProxyAdmin(admin.ModelAdmin):
    """Analytics Dashboard accessible from admin sidebar"""
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_module_permission(self, request):
        return request.user.is_staff
    
    def changelist_view(self, request, extra_context=None):
        """Override changelist to show analytics dashboard"""
        from apps.products.models import Product, ProductReview
        from apps.orders.models import Order, OrderItem, CartItem
        from apps.users.models import Wishlist
        
        # Calculate total revenue from delivered orders
        total_revenue = Order.objects.filter(
            status='delivered'
        ).aggregate(total=Sum('total'))['total'] or 0
        
        # Count orders by status
        total_orders = Order.objects.filter(status='delivered').count()
        pending_orders = Order.objects.filter(status='pending').count()
        
        # Order status distribution
        order_status_stats = Order.objects.values('status').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Most sold products (from delivered orders)
        most_sold_products = Product.objects.annotate(
            total_sold=Sum(
                'order_items__quantity',
                filter=Q(order_items__order__status='delivered')
            )
        ).filter(total_sold__gt=0).order_by('-total_sold')[:10]
        
        # Most wishlisted products
        most_wishlisted = Product.objects.annotate(
            wishlist_count=Count('wishlist')
        ).filter(wishlist_count__gt=0).order_by('-wishlist_count')[:10]
        
        # Most added to cart products
        most_in_cart = Product.objects.annotate(
            cart_count=Count('cart_items')
        ).filter(cart_count__gt=0).order_by('-cart_count')[:10]
        
        # Top rated products
        top_rated_products = Product.objects.annotate(
            avg_rating=Avg('reviews__rating'),
            total_reviews=Count('reviews')
        ).filter(total_reviews__gt=0).order_by('-avg_rating', '-total_reviews')[:10]
        
        # Recent reviews
        recent_reviews = ProductReview.objects.select_related(
            'product', 'user'
        ).order_by('-created_at')[:10]
        
        # Low stock products
        low_stock_products = Product.objects.filter(
            stock__lte=F('low_stock_threshold')
        ).order_by('stock')[:10]
        
        context = {
            **self.admin_site.each_context(request),
            'title': '📊 Analytics Dashboard',
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'order_status_stats': order_status_stats,
            'most_sold_products': most_sold_products,
            'most_wishlisted': most_wishlisted,
            'most_in_cart': most_in_cart,
            'top_rated_products': top_rated_products,
            'recent_reviews': recent_reviews,
            'low_stock_products': low_stock_products,
        }
        
        return render(request, 'admin/analytics_dashboard.html', context)
