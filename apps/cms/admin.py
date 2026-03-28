from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (
    SiteSettings, NavigationMenu, MegaMenuSettings, MegaMenuCategory, FooterColumn, FooterLink,
    Store, Testimonial, FAQ, Feature, Vendor,
    AboutHero, AboutSection, AboutStatistic, AboutImage,
    ContactSubmission,
    Page, Widget, PageWidget, WidgetHeroBanner, WidgetTextSection,
    WidgetStatistic, WidgetImage, WidgetFAQItem, WidgetHTMLContent,
    WidgetProductSection, WidgetDynamicHero
)


# ============================================================================
# HEADER & FOOTER MANAGEMENT
# ============================================================================

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'logo_preview', 'show_top_banner_status', 'updated_at')
    readonly_fields = ('logo_preview', 'footer_logo_preview', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name',),
            'description': 'Main site configuration'
        }),
        ('Logos', {
            'fields': ('site_logo', 'logo_preview', 'site_logo_footer', 'footer_logo_preview'),
            'description': 'Upload logos for header and footer'
        }),
        ('Top Banner (Header)', {
            'fields': ('top_banner_text', 'top_banner_bg_color', 'show_top_banner'),
            'description': 'Configure the promotional banner at the top of the site'
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'phone_description', 'email', 'address'),
            'description': 'Contact details displayed in header and footer'
        }),
        ('App Download Links', {
            'fields': ('app_download_title', 'app_download_subtitle', 'app_store_link', 'google_play_link'),
            'classes': ('collapse',),
            'description': 'Mobile app download section'
        }),
        ('Newsletter Section (Footer)', {
            'fields': ('newsletter_title', 'newsletter_description'),
            'description': 'Newsletter signup section in footer'
        }),
        ('Copyright (Footer)', {
            'fields': ('copyright_text',),
            'description': 'Copyright text displayed at bottom of footer'
        }),
        ('Social Media Links', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url'),
            'classes': ('collapse',),
            'description': 'Social media profile links'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
    
    def logo_preview(self, obj):
        if obj.site_logo:
            return format_html('<img src="{}" style="max-height: 60px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />', obj.site_logo.url)
        return mark_safe('<i class="fas fa-times-circle" style="color: red;"></i> No logo')
    logo_preview.short_description = mark_safe('<i class="fas fa-image"></i> Header Logo Preview')
    
    def footer_logo_preview(self, obj):
        if obj.site_logo_footer:
            return format_html('<img src="{}" style="max-height: 60px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />', obj.site_logo_footer.url)
        return mark_safe('<i class="fas fa-times-circle" style="color: red;"></i> No logo')
    footer_logo_preview.short_description = mark_safe('<i class="fas fa-image"></i> Footer Logo Preview')
    
    def show_top_banner_status(self, obj):
        if obj.show_top_banner:
            return mark_safe('<span style="color: green;"><i class="fas fa-check-circle"></i> Visible</span>')
        return mark_safe('<span style="color: red;"><i class="fas fa-times-circle"></i> Hidden</span>')
    show_top_banner_status.short_description = 'Top Banner'


@admin.register(NavigationMenu)
class NavigationMenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'custom_path', 'open_in_new_tab', 'parent', 'order', 'is_active', 'status_display', 'created_at')
    list_filter = ('is_active', 'parent', 'created_at')
    search_fields = ('title', 'url')
    list_editable = ('order', 'is_active')
    readonly_fields = ('created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Menu Item Details', {
            'fields': ('title', 'url', 'custom_path', 'open_in_new_tab', 'parent'),
            'description': 'Configure navigation menu item. Use URL like "/about", "/shop", "/contact" or page URLs from Page Builder'
        }),
        ('Settings', {
            'fields': ('order', 'is_active', 'created_at')
        }),
    )
    
    def status_display(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color: green;"><i class="fas fa-check-circle"></i> Active</span>')
        return mark_safe('<span style="color: red;"><i class="fas fa-times-circle"></i> Inactive</span>')
    status_display.short_description = 'Status'


@admin.register(MegaMenuSettings)
class MegaMenuSettingsAdmin(admin.ModelAdmin):
    list_display = ('description_preview', 'sale_badge_text', 'sale_badge_label', 'show_sale_badge', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Mega Menu Description', {
            'fields': ('description_text',),
            'description': 'Text displayed at the bottom of the categories mega menu'
        }),
        ('Sale Badge Settings', {
            'fields': ('sale_badge_label', 'sale_badge_text', 'show_sale_badge'),
            'description': 'Configure the "Best Seller / SALE" badge in the header'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return not MegaMenuSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
    
    def description_preview(self, obj):
        return obj.description_text[:50] + '...' if len(obj.description_text) > 50 else obj.description_text
    description_preview.short_description = 'Description'


@admin.register(MegaMenuCategory)
class MegaMenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'category_name', 'category_image_preview', 'is_active', 'status_display', 'created_at')
    list_display_links = ('category_name',)  # Make category_name the clickable link
    list_filter = ('is_active', 'created_at')
    search_fields = ('category__name',)
    list_editable = ('order', 'is_active')
    readonly_fields = ('created_at', 'category_image_preview')
    list_per_page = 9
    
    fieldsets = (
        ('Category Selection', {
            'fields': ('category', 'category_image_preview'),
            'description': 'Select a category to display in the mega menu (max 9 categories)'
        }),
        ('Settings', {
            'fields': ('order', 'is_active', 'created_at'),
            'description': 'Order determines the position (1-9) in the mega menu'
        }),
    )
    
    def category_name(self, obj):
        return obj.category.name
    category_name.short_description = 'Category'
    category_name.admin_order_field = 'category__name'
    
    def category_image_preview(self, obj):
        if obj.category.image:
            return format_html('<img src="{}" style="max-height: 60px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />', obj.category.image.url)
        return mark_safe('<i class="fas fa-times-circle" style="color: red;"></i> No image')
    category_image_preview.short_description = mark_safe('<i class="fas fa-image"></i> Category Image')
    
    def status_display(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color: green;"><i class="fas fa-check-circle"></i> Active</span>')
        return mark_safe('<span style="color: red;"><i class="fas fa-times-circle"></i> Inactive</span>')
    status_display.short_description = 'Status'


class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1
    fields = ('title', 'url', 'custom_path', 'open_in_new_tab', 'order', 'is_active')


@admin.register(FooterColumn)
class FooterColumnAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_count', 'order', 'is_active', 'status_display', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    list_editable = ('order', 'is_active')
    readonly_fields = ('created_at', 'link_count')
    inlines = [FooterLinkInline]
    list_per_page = 25
    
    fieldsets = (
        ('Column Information', {
            'fields': ('title',),
            'description': 'Footer column that will contain multiple links'
        }),
        ('Settings', {
            'fields': ('order', 'is_active', 'link_count', 'created_at')
        }),
    )
    
    def link_count(self, obj):
        count = obj.links.count()
        return format_html('<i class="fas fa-link"></i> <strong style="color: #2196F3;">{}</strong> links', count)
    link_count.short_description = mark_safe('<i class="fas fa-link"></i> Links')
    
    def status_display(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color: green;"><i class="fas fa-check-circle"></i> Active</span>')
        return mark_safe('<span style="color: red;"><i class="fas fa-times-circle"></i> Inactive</span>')
    status_display.short_description = 'Status'


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'column', 'url', 'order', 'is_active', 'status_display')
    list_filter = ('is_active', 'column')
    search_fields = ('title', 'url')
    list_editable = ('order', 'is_active')
    list_per_page = 25
    
    def status_display(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color: green;"><i class="fas fa-check-circle"></i> Active</span>')
        return mark_safe('<span style="color: red;"><i class="fas fa-times-circle"></i> Inactive</span>')
    status_display.short_description = 'Status'


# ============================================================================
# PAGE BUILDER SYSTEM
# ============================================================================

class PageWidgetInline(admin.TabularInline):
    model = PageWidget
    extra = 1
    fields = ['widget', 'order', 'is_active', 'config']
    autocomplete_fields = ['widget']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'page_url_display', 'widget_count', 'is_active', 'status_display', 'created_at', 'updated_at']
    list_editable = ['is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'slug', 'meta_description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'widget_count', 'page_url_display']
    inlines = [PageWidgetInline]
    
    fieldsets = (
        ('Page Information', {
            'fields': ('title', 'slug', 'meta_description'),
            'description': 'Create custom pages using widgets. After creating, add this page to Navigation Menu or Footer Links.'
        }),
        ('Page URL', {
            'fields': ('page_url_display',),
            'description': 'Copy this URL and add it to Navigation Menu or Footer Links'
        }),
        ('Status', {
            'fields': ('is_active', 'widget_count', 'created_at', 'updated_at')
        }),
    )
    
    def widget_count(self, obj):
        count = obj.page_widgets.filter(is_active=True).count()
        return format_html('<i class="fas fa-puzzle-piece"></i> <strong style="color: #4CAF50;">{}</strong> widgets', count)
    widget_count.short_description = mark_safe('<i class="fas fa-puzzle-piece"></i> Active Widgets')
    
    def page_url_display(self, obj):
        if obj.slug:
            url = f'/page/{obj.slug}/'
            return format_html(
                '<div style="background: #e3f2fd; padding: 10px; border-radius: 4px; border-left: 4px solid #2196F3;">'
                '<strong style="color: #1976d2;"><i class="fas fa-link"></i> {}</strong><br>'
                '<small style="color: #666;">Add this URL to Navigation Menu or Footer Links</small>'
                '</div>',
                url
            )
        return "Save page first to get URL"
    page_url_display.short_description = mark_safe('<i class="fas fa-link"></i> Page URL')
    
    def status_display(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color: green;"><i class="fas fa-check-circle"></i> Active</span>')
        return mark_safe('<span style="color: red;"><i class="fas fa-times-circle"></i> Inactive</span>')
    status_display.short_description = 'Status'


class WidgetStatisticInline(admin.TabularInline):
    model = WidgetStatistic
    extra = 1
    fields = ['number', 'label', 'order']


class WidgetImageInline(admin.TabularInline):
    model = WidgetImage
    extra = 1
    fields = ['image', 'alt_text', 'caption', 'order']


class WidgetFAQItemInline(admin.TabularInline):
    model = WidgetFAQItem
    extra = 1
    fields = ['question', 'answer', 'order']


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'widget_type_display', 'usage_count', 'is_active', 'status_display', 'created_at']
    list_editable = ['is_active']
    list_filter = ['widget_type', 'is_active', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at', 'usage_count']
    
    fieldsets = (
        ('Widget Information', {
            'fields': ('name', 'widget_type'),
            'description': 'Widgets are reusable content blocks that can be added to pages'
        }),
        ('Status', {
            'fields': ('is_active', 'usage_count', 'created_at', 'updated_at')
        }),
    )
    
    def get_inlines(self, request, obj=None):
        """Dynamically show inlines based on widget type"""
        if obj:
            if obj.widget_type in ['text_with_stats']:
                return [WidgetStatisticInline]
            elif obj.widget_type in ['two_column_images', 'image_gallery']:
                return [WidgetImageInline]
            elif obj.widget_type == 'faq_accordion':
                return [WidgetFAQItemInline]
        return []
    
    def usage_count(self, obj):
        count = obj.widget_pages.count()
        return format_html('<i class="fas fa-file-alt"></i> <strong style="color: #FF9800;">{}</strong> pages', count)
    usage_count.short_description = mark_safe('<i class="fas fa-file-alt"></i> Used in')
    
    def widget_type_display(self, obj):
        icons = {
            'dynamic_hero': '<i class="fas fa-bullseye"></i>',
            'hero_banner': '<i class="fas fa-bullseye"></i>',
            'image_banner': '<i class="fas fa-image"></i>',
            'text_section': '<i class="fas fa-align-left"></i>',
            'text_with_label': '<i class="fas fa-tag"></i>',
            'text_with_stats': '<i class="fas fa-chart-bar"></i>',
            'single_image': '<i class="fas fa-image"></i>',
            'two_column_images': '<i class="fas fa-images"></i>',
            'image_gallery': '<i class="fas fa-th"></i>',
            'features_grid': '<i class="fas fa-th-large"></i>',
            'testimonials_slider': '<i class="fas fa-comments"></i>',
            'vendors_showcase': '<i class="fas fa-store"></i>',
            'faq_accordion': '<i class="fas fa-question-circle"></i>',
            'contact_form': '<i class="fas fa-envelope"></i>',
            'store_locations': '<i class="fas fa-map-marker-alt"></i>',
            'product_section': '<i class="fas fa-shopping-bag"></i>',
            'featured_products': '<i class="fas fa-star"></i>',
            'product_categories': '<i class="fas fa-boxes"></i>',
            'product_slider': '<i class="fas fa-sliders-h"></i>',
            'html_content': '<i class="fas fa-code"></i>',
            'spacer': '<i class="fas fa-minus"></i>',
        }
        icon = icons.get(obj.widget_type, '<i class="fas fa-puzzle-piece"></i>')
        return mark_safe(f'{icon} {obj.get_widget_type_display()}')
    widget_type_display.short_description = 'Widget Type'
    
    def status_display(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color: green;"><i class="fas fa-check-circle"></i> Active</span>')
        return mark_safe('<span style="color: red;"><i class="fas fa-times-circle"></i> Inactive</span>')
    status_display.short_description = 'Status'


@admin.register(WidgetHeroBanner)
class WidgetHeroBannerAdmin(admin.ModelAdmin):
    list_display = ['widget', 'title', 'background_preview']
    search_fields = ['title', 'widget__name']
    readonly_fields = ['background_preview']
    autocomplete_fields = ['widget']
    
    def background_preview(self, obj):
        if obj.background_image:
            return format_html('<img src="{}" style="max-height: 100px; border-radius: 4px;" />', obj.background_image.url)
        return mark_safe('<i class="fas fa-times-circle" style="color: red;"></i> No image')
    background_preview.short_description = mark_safe('<i class="fas fa-image"></i> Preview')


@admin.register(WidgetTextSection)
class WidgetTextSectionAdmin(admin.ModelAdmin):
    list_display = ['widget', 'heading_short', 'text_align']
    search_fields = ['heading', 'content', 'widget__name']
    list_filter = ['text_align']
    autocomplete_fields = ['widget']
    
    def heading_short(self, obj):
        return obj.heading[:50] + '...' if len(obj.heading) > 50 else obj.heading
    heading_short.short_description = 'Heading'


@admin.register(WidgetHTMLContent)
class WidgetHTMLContentAdmin(admin.ModelAdmin):
    list_display = ['widget', 'css_classes']
    search_fields = ['widget__name', 'html_content']
    autocomplete_fields = ['widget']


@admin.register(PageWidget)
class PageWidgetAdmin(admin.ModelAdmin):
    list_display = ['page', 'widget', 'order', 'is_active', 'status_display']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'page']
    search_fields = ['page__title', 'widget__name']
    autocomplete_fields = ['page', 'widget']
    
    def status_display(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color: green;"><i class="fas fa-check-circle"></i> Active</span>')
        return mark_safe('<span style="color: red;"><i class="fas fa-times-circle"></i> Inactive</span>')
    status_display.short_description = 'Status'



# ============================================================================
# CONTENT SECTIONS
# ============================================================================

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('city', 'country', 'phone', 'email', 'is_active', 'status_display', 'order', 'created_at')
    list_filter = ('is_active', 'country', 'created_at')
    search_fields = ('city', 'country', 'address', 'phone', 'email')
    list_editable = ('is_active', 'order')
    readonly_fields = ('created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Location', {
            'fields': ('country', 'city', 'address')
        }),
        ('Contact', {
            'fields': ('phone', 'email')
        }),
        ('Settings', {
            'fields': ('order', 'is_active', 'created_at')
        }),
    )
    
    def status_display(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color: green;"><i class="fas fa-check-circle"></i> Active</span>')
        return mark_safe('<span style="color: red;"><i class="fas fa-times-circle"></i> Inactive</span>')
    status_display.short_description = 'Status'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_role', 'rating_display', 'is_active', 'status_display', 'order', 'created_at')
    list_filter = ('is_active', 'rating', 'created_at')
    search_fields = ('author_name', 'author_role', 'text')
    list_editable = ('is_active', 'order')
    readonly_fields = ('created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Author Information', {
            'fields': ('author_name', 'author_role')
        }),
        ('Testimonial', {
            'fields': ('text', 'rating')
        }),
        ('Settings', {
            'fields': ('order', 'is_active', 'created_at')
        }),
    )
    
    def rating_display(self, obj):
        stars = '<i class="fas fa-star" style="color: gold;"></i>' * obj.rating
        return format_html('<span>{}</span>', stars)
    rating_display.short_description = 'Rating'
    rating_display.admin_order_field = 'rating'
    
    def status_display(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color: green;"><i class="fas fa-check-circle"></i> Active</span>')
        return mark_safe('<span style="color: red;"><i class="fas fa-times-circle"></i> Inactive</span>')
    status_display.short_description = 'Status'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question_short', 'is_active', 'status_display', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('question', 'answer')
    list_editable = ('is_active', 'order')
    readonly_fields = ('created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('FAQ Content', {
            'fields': ('question', 'answer')
        }),
        ('Settings', {
            'fields': ('order', 'is_active', 'created_at')
        }),
    )
    
    def question_short(self, obj):
        return obj.question[:60] + '...' if len(obj.question) > 60 else obj.question
    question_short.short_description = 'Question'
    
    def status_display(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color: green;"><i class="fas fa-check-circle"></i> Active</span>')
        return mark_safe('<span style="color: red;"><i class="fas fa-times-circle"></i> Inactive</span>')
    status_display.short_description = 'Status'


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_name', 'is_active', 'status_display', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'icon_name')
    list_editable = ('is_active', 'order')
    readonly_fields = ('created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Feature Information', {
            'fields': ('title', 'description', 'icon_name')
        }),
        ('Settings', {
            'fields': ('order', 'is_active', 'created_at')
        }),
    )
    
    def status_display(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color: green;"><i class="fas fa-check-circle"></i> Active</span>')
        return mark_safe('<span style="color: red;"><i class="fas fa-times-circle"></i> Inactive</span>')
    status_display.short_description = 'Status'


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_preview', 'rating_display', 'review_count', 'is_active', 'status_display', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    readonly_fields = ('logo_preview', 'created_at')
    list_per_page = 25
    
    fieldsets = (
        ('Vendor Information', {
            'fields': ('name', 'description')
        }),
        ('Logo', {
            'fields': ('logo', 'logo_preview')
        }),
        ('Reviews', {
            'fields': ('rating', 'review_count', 'review_text')
        }),
        ('Settings', {
            'fields': ('is_active', 'created_at')
        }),
    )
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 80px; max-width: 80px; border-radius: 4px;" />', obj.logo.url)
        return mark_safe('<i class="fas fa-times-circle" style="color: red;"></i> No logo')
    logo_preview.short_description = mark_safe('<i class="fas fa-image"></i> Logo Preview')
    
    def rating_display(self, obj):
        stars = '<i class="fas fa-star" style="color: gold;"></i>' * int(obj.rating)
        return mark_safe(f'<span>{stars} {obj.rating}</span>')
    rating_display.short_description = 'Rating'
    rating_display.admin_order_field = 'rating'
    
    def status_display(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color: green;"><i class="fas fa-check-circle"></i> Active</span>')
        return mark_safe('<span style="color: red;"><i class="fas fa-times-circle"></i> Inactive</span>')
    status_display.short_description = 'Status'


# ============================================================================
# ABOUT PAGE
# ============================================================================

@admin.register(AboutHero)
class AboutHeroAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'status_display', 'created_at']
    list_editable = ['is_active']
    readonly_fields = ['background_preview', 'created_at']
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'background_image', 'background_preview')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at')
        }),
    )
    
    def background_preview(self, obj):
        if obj.background_image:
            return format_html('<img src="{}" style="max-height: 200px; border-radius: 4px;" />', obj.background_image.url)
        return mark_safe('<i class="fas fa-times-circle" style="color: red;"></i> No image')
    background_preview.short_description = mark_safe('<i class="fas fa-image"></i> Background Preview')
    
    def has_add_permission(self, request):
        return not AboutHero.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def status_display(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color: green;"><i class="fas fa-check-circle"></i> Active</span>')
        return mark_safe('<span style="color: red;"><i class="fas fa-times-circle"></i> Inactive</span>')
    status_display.short_description = 'Status'


class AboutStatisticInline(admin.TabularInline):
    model = AboutStatistic
    extra = 1
    fields = ['number', 'label', 'order']


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ['section_type', 'heading_short', 'order', 'is_active', 'status_display', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['section_type', 'is_active']
    search_fields = ['heading', 'content']
    readonly_fields = ['created_at']
    inlines = [AboutStatisticInline]
    fieldsets = (
        ('Section Type', {
            'fields': ('section_type',)
        }),
        ('Content', {
            'fields': ('label', 'heading', 'content')
        }),
        ('Display', {
            'fields': ('order', 'is_active', 'created_at')
        }),
    )
    
    def heading_short(self, obj):
        return obj.heading[:50] + '...' if len(obj.heading) > 50 else obj.heading
    heading_short.short_description = 'Heading'
    
    def status_display(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color: green;"><i class="fas fa-check-circle"></i> Active</span>')
        return mark_safe('<span style="color: red;"><i class="fas fa-times-circle"></i> Inactive</span>')
    status_display.short_description = 'Status'


@admin.register(AboutImage)
class AboutImageAdmin(admin.ModelAdmin):
    list_display = ['alt_text', 'image_preview', 'order', 'is_active', 'status_display', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['alt_text']
    readonly_fields = ['image_preview', 'created_at']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; border-radius: 4px;" />', obj.image.url)
        return mark_safe('<i class="fas fa-times-circle" style="color: red;"></i> No image')
    image_preview.short_description = mark_safe('<i class="fas fa-image"></i> Preview')
    
    def status_display(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color: green;"><i class="fas fa-check-circle"></i> Active</span>')
        return mark_safe('<span style="color: red;"><i class="fas fa-times-circle"></i> Inactive</span>')
    status_display.short_description = 'Status'


# ============================================================================
# CONTACT
# ============================================================================

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject_short', 'is_read', 'read_status', 'created_at']
    list_editable = ['is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    list_per_page = 50
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    def subject_short(self, obj):
        return obj.subject[:40] + '...' if len(obj.subject) > 40 else obj.subject
    subject_short.short_description = 'Subject'
    
    def read_status(self, obj):
        if obj.is_read:
            return mark_safe('<span style="color: green;"><i class="fas fa-check-circle"></i> Read</span>')
        return mark_safe('<span style="color: orange;"><i class="fas fa-envelope"></i> New</span>')
    read_status.short_description = 'Status'
    
    def has_add_permission(self, request):
        return False



@admin.register(WidgetProductSection)
class WidgetProductSectionAdmin(admin.ModelAdmin):
    list_display = ['widget', 'section_title', 'product_count']
    search_fields = ['section_title', 'widget__name']
    filter_horizontal = ['products']
    autocomplete_fields = ['widget']
    
    fieldsets = (
        ('Product Section', {
            'fields': ('widget', 'section_title'),
            'description': 'Create a product section with manual product selection. Products will display in a 4-column grid.'
        }),
        ('Products', {
            'fields': ('products',),
            'description': 'Select up to 8 products to display in this section'
        }),
    )
    
    def product_count(self, obj):
        count = obj.products.count()
        return format_html('<i class="fas fa-box"></i> <strong style="color: #4CAF50;">{}</strong> products', count)
    product_count.short_description = mark_safe('<i class="fas fa-boxes"></i> Products')


@admin.register(WidgetDynamicHero)
class WidgetDynamicHeroAdmin(admin.ModelAdmin):
    list_display = ['widget', 'title', 'show_discount_badge', 'show_button', 'show_price', 'background_preview']
    search_fields = ['title', 'widget__name']
    list_filter = ['show_discount_badge', 'show_button', 'show_price']
    readonly_fields = ['background_preview']
    autocomplete_fields = ['widget']
    
    fieldsets = (
        ('Hero Content', {
            'fields': ('widget', 'title', 'description', 'background_image', 'background_preview'),
            'description': 'Create a fully customizable hero banner like the homepage hero'
        }),
        ('Discount Badge (Optional)', {
            'fields': ('show_discount_badge', 'discount_percentage', 'discount_text'),
            'classes': ('collapse',),
            'description': 'Show a circular discount badge with percentage'
        }),
        ('Call-to-Action Button', {
            'fields': ('show_button', 'button_text', 'button_link'),
            'description': 'Add a button to drive user action'
        }),
        ('Price Section (Optional)', {
            'fields': ('show_price', 'price', 'price_text'),
            'classes': ('collapse',),
            'description': 'Display a price with custom text'
        }),
        ('Styling', {
            'fields': ('text_color', 'overlay_opacity'),
            'classes': ('collapse',),
            'description': 'Customize colors and overlay'
        }),
    )
    
    def background_preview(self, obj):
        if obj.background_image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 400px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />',
                obj.background_image.url
            )
        return mark_safe('<i class="fas fa-times-circle" style="color: red;"></i> No image')
    background_preview.short_description = mark_safe('<i class="fas fa-image"></i> Background Preview')
