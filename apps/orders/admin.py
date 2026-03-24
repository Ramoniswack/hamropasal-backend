from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Order, OrderItem, OrderStatusHistory, Cart, CartItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_sku', 'unit_price', 'discount_price', 'quantity', 'subtotal')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ('status', 'notes', 'changed_by', 'created_at')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'user', 'customer_name', 'status_display',
        'payment_status_display', 'total_display', 'item_count',
        'created_at'
    )
    list_filter = ('status', 'payment_status', 'created_at', 'updated_at')
    search_fields = ('order_number', 'user__username', 'customer_name', 'customer_email', 'customer_phone')
    readonly_fields = (
        'order_number', 'user', 'subtotal', 'shipping_cost', 'tax', 'discount', 'total',
        'created_at', 'updated_at', 'confirmed_at', 'shipped_at', 'delivered_at',
        'item_count', 'total_quantity'
    )
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    list_per_page = 25
    date_hierarchy = 'created_at'
    actions = ['mark_as_confirmed', 'mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'payment_status')
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Shipping Address', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip_code', 'shipping_country')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'shipping_cost', 'tax', 'discount', 'total')
        }),
        ('Additional Information', {
            'fields': ('notes', 'coupon_code'),
            'classes': ('collapse',)
        }),
        ('Order Summary', {
            'fields': ('item_count', 'total_quantity'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'shipped_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_display(self, obj):
        colors = {
            'pending': 'orange',
            'confirmed': 'blue',
            'processing': 'purple',
            'shipped': 'teal',
            'delivered': 'green',
            'cancelled': 'red',
            'refunded': 'gray'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_display.short_description = 'Status'
    status_display.admin_order_field = 'status'
    
    def payment_status_display(self, obj):
        colors = {
            'pending': 'orange',
            'paid': 'green',
            'failed': 'red',
            'refunded': 'gray'
        }
        color = colors.get(obj.payment_status, 'black')
        return format_html(
            '<span style="color: {};">{}</span>',
            color, obj.get_payment_status_display()
        )
    payment_status_display.short_description = 'Payment'
    payment_status_display.admin_order_field = 'payment_status'
    
    def total_display(self, obj):
        return format_html('<strong>${:,.2f}</strong>', obj.total)
    total_display.short_description = 'Total'
    total_display.admin_order_field = 'total'
    
    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            # Create status history entry
            OrderStatusHistory.objects.create(
                order=obj,
                status=obj.status,
                changed_by=request.user,
                notes=f"Status changed to {obj.get_status_display()}"
            )
            
            # Update timestamp fields
            if obj.status == 'confirmed' and not obj.confirmed_at:
                obj.confirmed_at = timezone.now()
            elif obj.status == 'shipped' and not obj.shipped_at:
                obj.shipped_at = timezone.now()
            elif obj.status == 'delivered' and not obj.delivered_at:
                obj.delivered_at = timezone.now()
        
        super().save_model(request, obj, form, change)
    
    def mark_as_confirmed(self, request, queryset):
        for order in queryset:
            order.status = 'confirmed'
            order.confirmed_at = timezone.now()
            order.save()
            OrderStatusHistory.objects.create(
                order=order,
                status='confirmed',
                changed_by=request.user,
                notes="Bulk action: Marked as confirmed"
            )
        self.message_user(request, f'{queryset.count()} orders marked as confirmed.')
    mark_as_confirmed.short_description = 'Mark as Confirmed'
    
    def mark_as_processing(self, request, queryset):
        for order in queryset:
            order.status = 'processing'
            order.save()
            OrderStatusHistory.objects.create(
                order=order,
                status='processing',
                changed_by=request.user,
                notes="Bulk action: Marked as processing"
            )
        self.message_user(request, f'{queryset.count()} orders marked as processing.')
    mark_as_processing.short_description = 'Mark as Processing'
    
    def mark_as_shipped(self, request, queryset):
        for order in queryset:
            order.status = 'shipped'
            order.shipped_at = timezone.now()
            order.save()
            OrderStatusHistory.objects.create(
                order=order,
                status='shipped',
                changed_by=request.user,
                notes="Bulk action: Marked as shipped"
            )
        self.message_user(request, f'{queryset.count()} orders marked as shipped.')
    mark_as_shipped.short_description = 'Mark as Shipped'
    
    def mark_as_delivered(self, request, queryset):
        for order in queryset:
            order.status = 'delivered'
            order.delivered_at = timezone.now()
            order.save()
            OrderStatusHistory.objects.create(
                order=order,
                status='delivered',
                changed_by=request.user,
                notes="Bulk action: Marked as delivered"
            )
        self.message_user(request, f'{queryset.count()} orders marked as delivered.')
    mark_as_delivered.short_description = 'Mark as Delivered'
    
    def mark_as_cancelled(self, request, queryset):
        for order in queryset:
            order.status = 'cancelled'
            order.save()
            OrderStatusHistory.objects.create(
                order=order,
                status='cancelled',
                changed_by=request.user,
                notes="Bulk action: Marked as cancelled"
            )
        self.message_user(request, f'{queryset.count()} orders marked as cancelled.')
    mark_as_cancelled.short_description = 'Mark as Cancelled'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'quantity', 'unit_price_display', 'subtotal_display')
    list_filter = ('created_at',)
    search_fields = ('order__order_number', 'product_name', 'product_sku')
    readonly_fields = ('order', 'product', 'product_name', 'product_sku', 'quantity', 'unit_price', 'discount_price', 'subtotal', 'created_at')
    
    def unit_price_display(self, obj):
        return f'${obj.unit_price}'
    unit_price_display.short_description = 'Unit Price'
    
    def subtotal_display(self, obj):
        return f'${obj.subtotal}'
    subtotal_display.short_description = 'Subtotal'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'status_display', 'changed_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order__order_number', 'notes')
    readonly_fields = ('order', 'status', 'notes', 'changed_by', 'created_at')
    
    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = 'Status'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'unit_price', 'subtotal', 'created_at', 'updated_at')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_display', 'item_count', 'total_quantity', 'subtotal_display', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'session_key')
    readonly_fields = ('user', 'session_key', 'item_count', 'total_quantity', 'subtotal', 'created_at', 'updated_at')
    inlines = [CartItemInline]
    
    def user_display(self, obj):
        if obj.user:
            return obj.user.username
        return f"Guest ({obj.session_key[:8]}...)"
    user_display.short_description = 'User'
    
    def subtotal_display(self, obj):
        return f'${obj.subtotal:,.2f}'
    subtotal_display.short_description = 'Subtotal'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'unit_price_display', 'subtotal_display', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('cart__user__username', 'product__name')
    readonly_fields = ('cart', 'product', 'unit_price', 'subtotal', 'created_at', 'updated_at')
    
    def unit_price_display(self, obj):
        return f'${obj.unit_price}'
    unit_price_display.short_description = 'Unit Price'
    
    def subtotal_display(self, obj):
        return f'${obj.subtotal}'
    subtotal_display.short_description = 'Subtotal'
