from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings, NavigationMenu, FooterColumn, FooterLink,
    Store, Testimonial, FAQ, Feature, Vendor,
    AboutHero, AboutSection, AboutStatistic, AboutImage,
    ContactSubmission,
    Page, Widget, PageWidget, WidgetHeroBanner, WidgetTextSection,
    WidgetStatistic, WidgetImage, WidgetFAQItem, WidgetHTMLContent
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'logo_preview', 'show_top_banner', 'updated_at')
    readonly_fields = ('logo_preview', 'footer_logo_preview', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name',),
            'description': 'Main site configuration'
        }),
        ('Logos', {
            'fields': ('site_logo', 'logo_preview', 'site_logo_footer', 'footer_logo_preview')
        }),
        ('Header Settings', {
            'fields': ('top_banner_text', 'top_banner_bg_color', 'show_top_banner')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'phone_description', 'email', 'address')
        }),
        ('App Download', {
            'fields': ('app_download_title', 'app_download_subtitle', 'app_store_link', 'google_play_link'),
            'classes': ('collapse',)
        }),
        ('Newsletter', {
            'fields': ('newsletter_title', 'newsletter_description')
        }),
        ('Footer', {
            'fields': ('copyright_text',)
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False
    
    def logo_preview(self, obj):
        if obj.site_logo:
            return format_html('<img src="{}" style="max-height: 60px;" />', obj.site_logo.url)
        return "No logo"
    logo_preview.short_description = 'Header Logo Preview'
    
    def footer_logo_preview(self, obj):
        if obj.site_logo_footer:
            return format_html('<img src="{}" style="max-height: 60px;" />', obj.site_logo_footer.url)
        return "No logo"
    footer_logo_preview.short_description = 'Footer Logo Preview'


@admin.register(NavigationMenu)
class NavigationMenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'custom_path', 'open_in_new_tab', 'parent', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'parent', 'created_at')
    search_fields = ('title', 'url')
    list_editable = ('order', 'is_active')
    readonly_fields = ('created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Menu Item', {
            'fields': ('title', 'url', 'custom_path', 'open_in_new_tab', 'parent')
        }),
        ('Settings', {
            'fields': ('order', 'is_active', 'created_at')
        }),
    )


class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1
    fields = ('title', 'url', 'custom_path', 'open_in_new_tab', 'order', 'is_active')


@admin.register(FooterColumn)
class FooterColumnAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_count', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    list_editable = ('order', 'is_active')
    readonly_fields = ('created_at', 'link_count')
    inlines = [FooterLinkInline]
    list_per_page = 25
    
    fieldsets = (
        ('Column Information', {
            'fields': ('title',)
        }),
        ('Settings', {
            'fields': ('order', 'is_active', 'link_count', 'created_at')
        }),
    )
    
    def link_count(self, obj):
        count = obj.links.count()
        return format_html('<strong>{}</strong> links', count)
    link_count.short_description = 'Links'


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'column', 'url', 'order', 'is_active')
    list_filter = ('is_active', 'column')
    search_fields = ('title', 'url')
    list_editable = ('order', 'is_active')
    list_per_page = 25


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('city', 'country', 'phone', 'email', 'is_active', 'order', 'created_at')
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


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_role', 'rating_display', 'is_active', 'order', 'created_at')
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
        stars = '⭐' * obj.rating
        return format_html('<span style="color: gold;">{}</span>', stars)
    rating_display.short_description = 'Rating'
    rating_display.admin_order_field = 'rating'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question_short', 'is_active', 'order', 'created_at')
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


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_name', 'is_active', 'order', 'created_at')
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


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_preview', 'rating_display', 'review_count', 'is_active', 'created_at')
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
            return format_html('<img src="{}" style="max-height: 80px; max-width: 80px;" />', obj.logo.url)
        return "No logo"
    logo_preview.short_description = 'Logo Preview'
    
    def rating_display(self, obj):
        stars = '⭐' * int(obj.rating)
        return format_html('<span style="color: gold;">{}</span> {}', stars, obj.rating)
    rating_display.short_description = 'Rating'
    rating_display.admin_order_field = 'rating'



# About Page Admin
@admin.register(AboutHero)
class AboutHeroAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
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
            return format_html('<img src="{}" style="max-height: 200px;" />', obj.background_image.url)
        return "No image"
    background_preview.short_description = 'Background Preview'
    
    def has_add_permission(self, request):
        return not AboutHero.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


class AboutStatisticInline(admin.TabularInline):
    model = AboutStatistic
    extra = 1
    fields = ['number', 'label', 'order']


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ['section_type', 'heading_short', 'order', 'is_active', 'created_at']
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


@admin.register(AboutImage)
class AboutImageAdmin(admin.ModelAdmin):
    list_display = ['alt_text', 'image_preview', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['alt_text']
    readonly_fields = ['image_preview', 'created_at']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject_short', 'is_read', 'created_at']
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
    
    def has_add_permission(self, request):
        return False



# Widget-Based Page Builder Admin
class PageWidgetInline(admin.TabularInline):
    model = PageWidget
    extra = 1
    fields = ['widget', 'order', 'is_active', 'config']
    autocomplete_fields = ['widget']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'widget_count', 'is_active', 'created_at', 'updated_at']
    list_editable = ['is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'slug', 'meta_description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'widget_count']
    inlines = [PageWidgetInline]
    
    fieldsets = (
        ('Page Information', {
            'fields': ('title', 'slug', 'meta_description')
        }),
        ('Status', {
            'fields': ('is_active', 'widget_count', 'created_at', 'updated_at')
        }),
    )
    
    def widget_count(self, obj):
        count = obj.page_widgets.filter(is_active=True).count()
        return format_html('<strong>{}</strong> widgets', count)
    widget_count.short_description = 'Active Widgets'


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
    list_display = ['name', 'widget_type', 'usage_count', 'is_active', 'created_at']
    list_editable = ['is_active']
    list_filter = ['widget_type', 'is_active', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at', 'usage_count']
    
    fieldsets = (
        ('Widget Information', {
            'fields': ('name', 'widget_type')
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
        return format_html('<strong>{}</strong> pages', count)
    usage_count.short_description = 'Used in'


@admin.register(WidgetHeroBanner)
class WidgetHeroBannerAdmin(admin.ModelAdmin):
    list_display = ['widget', 'title', 'background_preview']
    search_fields = ['title', 'widget__name']
    readonly_fields = ['background_preview']
    autocomplete_fields = ['widget']
    
    def background_preview(self, obj):
        if obj.background_image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.background_image.url)
        return "No image"
    background_preview.short_description = 'Preview'


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
    list_display = ['page', 'widget', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'page']
    search_fields = ['page__title', 'widget__name']
    autocomplete_fields = ['page', 'widget']
