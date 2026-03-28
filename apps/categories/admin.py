from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview', 'slug', 'parent', 'product_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'parent', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'image_preview', 'product_count')
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'parent')
        }),
        ('Image', {
            'fields': ('image', 'image_preview')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Information', {
            'fields': ('product_count', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Image Preview'
    
    def product_count(self, obj):
        count = obj.products.count()
        return format_html('<strong>{}</strong> products', count)
    product_count.short_description = 'Products'
