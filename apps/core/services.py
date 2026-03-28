"""
Analytics and Business Logic Services
Handles all analytics calculations and aggregations
"""
from django.db.models import Sum, Count, Avg, F, Q, DecimalField
from django.db.models.functions import TruncDate, TruncMonth, Coalesce
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


class AnalyticsService:
    """Service for calculating eCommerce analytics"""
    
    @staticmethod
    def get_dashboard_kpis():
        """Get key performance indicators for dashboard"""
        from apps.orders.models import Order
        from apps.products.models import Product
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        month_start = today.replace(day=1)
        
        try:
            # Today's metrics
            today_orders = Order.objects.filter(created_at__date=today)
            today_revenue = today_orders.aggregate(
                total=Sum('total')
            )['total'] or Decimal('0.00')
            today_order_count = today_orders.count()
            
            # Yesterday's metrics for comparison
            yesterday_orders = Order.objects.filter(created_at__date=yesterday)
            yesterday_revenue = yesterday_orders.aggregate(
                total=Sum('total')
            )['total'] or Decimal('0.00')
            yesterday_order_count = yesterday_orders.count()
            
            # Month metrics
            month_orders = Order.objects.filter(created_at__date__gte=month_start)
            month_revenue = month_orders.aggregate(
                total=Sum('total')
            )['total'] or Decimal('0.00')
            month_order_count = month_orders.count()
            
            # All time metrics
            total_orders = Order.objects.count()
            total_revenue = Order.objects.aggregate(
                total=Sum('total')
            )['total'] or Decimal('0.00')
            
            # Average order value
            avg_order_value = Order.objects.aggregate(
                avg=Avg('total')
            )['avg'] or Decimal('0.00')
            
            # Total customers
            total_customers = User.objects.filter(is_staff=False, is_superuser=False).count()
            
            # New customers this month
            new_customers_month = User.objects.filter(
                is_staff=False,
                is_superuser=False,
                date_joined__date__gte=month_start
            ).count()
            
            # Product metrics
            total_products = Product.objects.filter(is_active=True).count()
            
            # Low stock products
            low_stock_count = Product.objects.filter(
                stock__lte=F('low_stock_threshold'),
                stock__gt=0,
                is_active=True
            ).count()
            
            # Out of stock products
            out_of_stock_count = Product.objects.filter(
                stock=0,
                is_active=True
            ).count()
            
            # Calculate percentage changes
            revenue_change = AnalyticsService._calculate_percentage_change(
                float(today_revenue), float(yesterday_revenue)
            )
            orders_change = AnalyticsService._calculate_percentage_change(
                today_order_count, yesterday_order_count
            )
            
            return {
                'today_revenue': float(today_revenue),
                'today_orders': today_order_count,
                'month_revenue': float(month_revenue),
                'month_orders': month_order_count,
                'total_orders': total_orders,
                'total_revenue': float(total_revenue),
                'avg_order_value': float(avg_order_value),
                'total_customers': total_customers,
                'new_customers_month': new_customers_month,
                'total_products': total_products,
                'low_stock_count': low_stock_count,
                'out_of_stock_count': out_of_stock_count,
                'revenue_change': revenue_change,
                'orders_change': orders_change,
            }
        except Exception as e:
            print(f"Error in get_dashboard_kpis: {e}")
            return {
                'today_revenue': 0.0,
                'today_orders': 0,
                'month_revenue': 0.0,
                'month_orders': 0,
                'total_orders': 0,
                'total_revenue': 0.0,
                'avg_order_value': 0.0,
                'total_customers': 0,
                'new_customers_month': 0,
                'total_products': 0,
                'low_stock_count': 0,
                'out_of_stock_count': 0,
                'revenue_change': 0.0,
                'orders_change': 0.0,
            }
    
    @staticmethod
    def get_revenue_by_day(days=30):
        """Get revenue grouped by day for the last N days"""
        from apps.orders.models import Order
        
        try:
            start_date = timezone.now().date() - timedelta(days=days)
            
            revenue_data = Order.objects.filter(
                created_at__date__gte=start_date
            ).annotate(
                date=TruncDate('created_at')
            ).values('date').annotate(
                revenue=Sum('total')
            ).order_by('date')
            
            return [
                {
                    'date': item['date'].strftime('%Y-%m-%d'),
                    'revenue': float(item['revenue'] or 0)
                }
                for item in revenue_data
            ]
        except Exception as e:
            print(f"Error in get_revenue_by_day: {e}")
            return []
    
    @staticmethod
    def get_orders_by_day(days=30):
        """Get order count grouped by day for the last N days"""
        from apps.orders.models import Order
        
        try:
            start_date = timezone.now().date() - timedelta(days=days)
            
            orders_data = Order.objects.filter(
                created_at__date__gte=start_date
            ).annotate(
                date=TruncDate('created_at')
            ).values('date').annotate(
                count=Count('id')
            ).order_by('date')
            
            return [
                {
                    'date': item['date'].strftime('%Y-%m-%d'),
                    'count': item['count']
                }
                for item in orders_data
            ]
        except Exception as e:
            print(f"Error in get_orders_by_day: {e}")
            return []
    
    @staticmethod
    def get_revenue_by_category():
        """Get revenue grouped by product category"""
        from apps.orders.models import OrderItem
        
        try:
            category_revenue = OrderItem.objects.select_related(
                'product__category'
            ).values(
                'product__category__name'
            ).annotate(
                revenue=Sum(F('quantity') * F('price'))
            ).order_by('-revenue')[:10]
            
            return [
                {
                    'category': item['product__category__name'] or 'Uncategorized',
                    'revenue': float(item['revenue'] or 0)
                }
                for item in category_revenue
            ]
        except Exception as e:
            print(f"Error in get_revenue_by_category: {e}")
            return []
    
    @staticmethod
    def get_top_selling_products(limit=10):
        """Get top selling products by units sold"""
        from apps.products.models import Product
        
        try:
            top_products = Product.objects.filter(
                units_sold__gt=0
            ).order_by('-units_sold')[:limit]
            
            return [
                {
                    'name': product.name,
                    'units_sold': product.units_sold,
                    'revenue': float(product.revenue_generated or 0)
                }
                for product in top_products
            ]
        except Exception as e:
            print(f"Error in get_top_selling_products: {e}")
            return []
    
    @staticmethod
    def get_customer_growth(months=6):
        """Get customer growth over time"""
        from django.contrib.auth import get_user_model
        
        try:
            User = get_user_model()
            start_date = timezone.now().date() - timedelta(days=months*30)
            
            customer_data = User.objects.filter(
                is_staff=False,
                is_superuser=False,
                date_joined__date__gte=start_date
            ).annotate(
                month=TruncMonth('date_joined')
            ).values('month').annotate(
                count=Count('id')
            ).order_by('month')
            
            return [
                {
                    'month': item['month'].strftime('%Y-%m'),
                    'count': item['count']
                }
                for item in customer_data
            ]
        except Exception as e:
            print(f"Error in get_customer_growth: {e}")
            return []
    
    @staticmethod
    def get_order_status_distribution():
        """Get distribution of orders by status"""
        from apps.orders.models import Order
        
        try:
            status_data = Order.objects.values('status').annotate(
                count=Count('id')
            ).order_by('-count')
            
            return [
                {
                    'status': item['status'].replace('_', ' ').title(),
                    'count': item['count']
                }
                for item in status_data
            ]
        except Exception as e:
            print(f"Error in get_order_status_distribution: {e}")
            return []
    
    @staticmethod
    def get_low_stock_products(limit=10):
        """Get products with low stock"""
        from apps.products.models import Product
        
        try:
            low_stock = Product.objects.filter(
                stock__lte=F('low_stock_threshold'),
                stock__gt=0,
                is_active=True
            ).order_by('stock')[:limit]
            
            return [
                {
                    'name': product.name,
                    'stock': product.stock,
                    'threshold': product.low_stock_threshold
                }
                for product in low_stock
            ]
        except Exception as e:
            print(f"Error in get_low_stock_products: {e}")
            return []
    
    @staticmethod
    def _calculate_percentage_change(current, previous):
        """Calculate percentage change between two values"""
        if previous == 0:
            return 100.0 if current > 0 else 0.0
        return round(((current - previous) / previous) * 100, 2)
