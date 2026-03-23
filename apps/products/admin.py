from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductImage


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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_display', 'discount_display', 'stock', 'is_featured', 'is_active', 'created_at')
    list_filter = ('is_featured', 'is_active', 'category', 'created_at')
    search_fields = ('name', 'slug', 'description', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_featured', 'is_active', 'stock')
    readonly_fields = ('created_at', 'updated_at', 'final_price', 'discount_percentage')
    inlines = [ProductImageInline]
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category')
        }),
        ('Description', {
            'fields': ('short_description', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'discount_price', 'final_price', 'discount_percentage', 'stock')
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
    discount_display.short_description = 'Discount Price'
    discount_display.admin_order_field = 'discount_price'


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
