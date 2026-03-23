from django.contrib import admin
from django.utils.html import format_html
from .models import HeroBanner, MarketplaceBanner, PromoBanner, ScrollingBanner


@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ('title_short', 'image_preview', 'discount_percentage', 'price', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active', 'order')
    readonly_fields = ('image_preview', 'created_at')
    list_per_page = 25
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description')
        }),
        ('Image', {
            'fields': ('image', 'image_preview')
        }),
        ('Discount Information', {
            'fields': ('discount_percentage', 'discount_text')
        }),
        ('Pricing', {
            'fields': ('price', 'price_text')
        }),
        ('Button', {
            'fields': ('button_text', 'button_link')
        }),
        ('Settings', {
            'fields': ('order', 'is_active', 'created_at')
        }),
    )
    
    def title_short(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    title_short.short_description = 'Title'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 200px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(MarketplaceBanner)
class MarketplaceBannerAdmin(admin.ModelAdmin):
    list_display = ('title_short', 'image_preview', 'button_text', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active', 'order')
    readonly_fields = ('image_preview', 'created_at')
    list_per_page = 25
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description')
        }),
        ('Image', {
            'fields': ('image', 'image_preview')
        }),
        ('Button', {
            'fields': ('button_text', 'button_link')
        }),
        ('Settings', {
            'fields': ('order', 'is_active', 'created_at')
        }),
    )
    
    def title_short(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    title_short.short_description = 'Title'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px; max-width: 150px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(PromoBanner)
class PromoBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'button_text', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active',)
    readonly_fields = ('image_preview', 'created_at')
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description')
        }),
        ('Image', {
            'fields': ('image', 'image_preview')
        }),
        ('Button', {
            'fields': ('button_text', 'button_link')
        }),
        ('Settings', {
            'fields': ('is_active', 'created_at')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px; max-width: 200px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(ScrollingBanner)
class ScrollingBannerAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('text',)
    list_editable = ('is_active',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Content', {
            'fields': ('text',)
        }),
        ('Settings', {
            'fields': ('is_active', 'created_at')
        }),
    )
