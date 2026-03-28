from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Avg, Count
from .models import (
    Product, ProductImage, ProductTag, ProductTagAssignment,
    NutritionalFact, ProductFeature, RelatedProduct,
    ProductReview, StockHistory, RecentlyViewed
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'image_preview', 'is_primary')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'


class ProductTagAssignmentInline(admin.TabularInline):
    model = ProductTagAssignment
    extra = 1
    autocomplete_fields = ['tag']


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 1
    fields = ('title', 'icon', 'order')


class RelatedProductInline(admin.TabularInline):
    model = RelatedProduct
    fk_name = 'product'
    extra = 1
    autocomplete_fields = ['related_product']
    fields = ('related_product', 'order')


class NutritionalFactInline(admin.StackedInline):
    model = NutritionalFact
    extra = 0
    fields = (
        ('protein_grams', 'protein_percentage'),
        ('carbohydrates_grams', 'carbohydrates_percentage'),
        ('fats_grams', 'fats_percentage'),
        ('calories', 'serving_size'),
        'disclaimer'
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'sku', 'category', 'price_display', 'discount_display',
        'stock_status', 'units_sold', 'revenue_display', 'rating_display',
        'is_featured', 'is_active', 'created_at'
    )
    list_filter = ('is_featured', 'is_active', 'category', 'created_at')
    search_fields = ('name', 'slug', 'sku', 'description', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_featured', 'is_active')
    readonly_fields = (
        'sku', 'created_at', 'updated_at', 'final_price', 'discount_percentage',
        'units_sold', 'revenue_generated', 'average_rating', 'review_count'
    )
    inlines = [
        ProductImageInline,
        NutritionalFactInline,
        ProductFeatureInline,
        ProductTagAssignmentInline,
        RelatedProductInline
    ]
    list_per_page = 25
    date_hierarchy = 'created_at'
    actions = ['mark_as_featured', 'mark_as_not_featured', 'activate_products', 'deactivate_products']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'category')
        }),
        ('Description', {
            'fields': ('short_description', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'discount_price', 'final_price', 'discount_percentage')
        }),
        ('Inventory', {
            'fields': ('stock', 'low_stock_threshold')
        }),
        ('Sales Analytics', {
            'fields': ('units_sold', 'revenue_generated'),
            'classes': ('collapse',)
        }),
        ('Reviews', {
            'fields': ('average_rating', 'review_count'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def price_display(self, obj):
        return f'${obj.price}'
    price_display.short_description = 'Price'
    price_display.admin_order_field = 'price'
    
    def discount_display(self, obj):
        if obj.discount_price:
            return format_html('<span style="color: green;">${}</span>', obj.discount_price)
        return '-'
    discount_display.short_description = 'Discount'
    discount_display.admin_order_field = 'discount_price'
    
    def stock_status(self, obj):
        if obj.stock == 0:
            return format_html('<span style="color: red; font-weight: bold;">OUT OF STOCK</span>')
        elif obj.is_low_stock:
            return format_html('<span style="color: orange; font-weight: bold;">{} (LOW)</span>', obj.stock)
        return format_html('<span style="color: green;">{}</span>', obj.stock)
    stock_status.short_description = 'Stock'
    stock_status.admin_order_field = 'stock'
    
    def revenue_display(self, obj):
        return f'${obj.revenue_generated:,.2f}'
    revenue_display.short_description = 'Revenue'
    revenue_display.admin_order_field = 'revenue_generated'
    
    def rating_display(self, obj):
        avg = obj.average_rating
        count = obj.review_count
        if count > 0:
            return mark_safe(f'<i class="fas fa-star" style="color: #f39c12;"></i> {avg} ({count} reviews)')
        return '-'
    rating_display.short_description = 'Rating'
    
    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} products marked as featured.')
    mark_as_featured.short_description = 'Mark selected as featured'
    
    def mark_as_not_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} products unmarked as featured.')
    mark_as_not_featured.short_description = 'Unmark selected as featured'
    
    def activate_products(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} products activated.')
    activate_products.short_description = 'Activate selected products'
    
    def deactivate_products(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} products deactivated.')
    deactivate_products.short_description = 'Deactivate selected products'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('product__name',)
    list_editable = ('is_primary',)
    readonly_fields = ('image_preview', 'created_at')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)
    
    def product_count(self, obj):
        return obj.product_assignments.count()
    product_count.short_description = 'Products'


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating_display', 'is_verified_purchase', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'is_approved', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at', 'updated_at', 'helpful_count')
    actions = ['approve_reviews', 'unapprove_reviews']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('product', 'user', 'rating', 'title', 'comment')
        }),
        ('Status', {
            'fields': ('is_verified_purchase', 'is_approved', 'helpful_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def rating_display(self, obj):
        stars_html = ''.join(['<i class="fas fa-star" style="color: #f39c12;"></i>' for _ in range(obj.rating)])
        empty_stars = ''.join(['<i class="far fa-star" style="color: #ddd;"></i>' for _ in range(5 - obj.rating)])
        return mark_safe(f'<span title="{obj.rating}/5">{stars_html}{empty_stars}</span>')
    rating_display.short_description = 'Rating'
    rating_display.admin_order_field = 'rating'
    
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} reviews approved.')
    approve_reviews.short_description = 'Approve selected reviews'
    
    def unapprove_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} reviews unapproved.')
    unapprove_reviews.short_description = 'Unapprove selected reviews'


@admin.register(StockHistory)
class StockHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'change_type', 'quantity_change_display', 'stock_before', 'stock_after', 'created_by', 'created_at')
    list_filter = ('change_type', 'created_at')
    search_fields = ('product__name', 'notes')
    readonly_fields = ('product', 'change_type', 'quantity_change', 'stock_before', 'stock_after', 'created_by', 'created_at')
    date_hierarchy = 'created_at'
    
    def quantity_change_display(self, obj):
        if obj.quantity_change > 0:
            return format_html('<span style="color: green;">+{}</span>', obj.quantity_change)
        return format_html('<span style="color: red;">{}</span>', obj.quantity_change)
    quantity_change_display.short_description = 'Change'
    quantity_change_display.admin_order_field = 'quantity_change'
    
    def has_add_permission(self, request):
        return False  # Stock history is created automatically
    
    def has_delete_permission(self, request, obj=None):
        return False  # Don't allow deletion of history


@admin.register(NutritionalFact)
class NutritionalFactAdmin(admin.ModelAdmin):
    list_display = ('product', 'calories', 'protein_grams', 'carbohydrates_grams', 'fats_grams')
    search_fields = ('product__name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ('product', 'title', 'icon', 'order')
    list_filter = ('icon',)
    search_fields = ('product__name', 'title')
    list_editable = ('order',)


@admin.register(RelatedProduct)
class RelatedProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'related_product', 'order')
    search_fields = ('product__name', 'related_product__name')
    list_editable = ('order',)
    autocomplete_fields = ['product', 'related_product']



@admin.register(RecentlyViewed)
class RecentlyViewedAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'session_key_short', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['product__name', 'user__username', 'user__email', 'session_key']
    readonly_fields = ['viewed_at']
    date_hierarchy = 'viewed_at'
    
    def session_key_short(self, obj):
        if obj.session_key:
            return f"{obj.session_key[:8]}..."
        return "-"
    session_key_short.short_description = 'Session'
