from rest_framework import serializers
from .models import (
    SiteSettings, NavigationMenu, FooterColumn, FooterLink,
    Store, Testimonial, FAQ, Feature, Vendor,
    AboutHero, AboutSection, AboutStatistic, AboutImage,
    ContactSubmission,
    Page, Widget, PageWidget, WidgetHeroBanner, WidgetTextSection,
    WidgetStatistic, WidgetImage, WidgetFAQItem, WidgetHTMLContent
)


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = '__all__'


class NavigationMenuSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    final_url = serializers.SerializerMethodField()
    
    class Meta:
        model = NavigationMenu
        fields = ['id', 'title', 'url', 'custom_path', 'final_url', 'open_in_new_tab', 'order', 'is_active', 'parent', 'children']
    
    def get_children(self, obj):
        if obj.children.exists():
            return NavigationMenuSerializer(obj.children.filter(is_active=True), many=True).data
        return []
    
    def get_final_url(self, obj):
        return obj.get_url()


class FooterLinkSerializer(serializers.ModelSerializer):
    final_url = serializers.SerializerMethodField()
    
    class Meta:
        model = FooterLink
        fields = ['id', 'title', 'url', 'custom_path', 'final_url', 'open_in_new_tab', 'order', 'is_active']
    
    def get_final_url(self, obj):
        return obj.get_url()


class FooterColumnSerializer(serializers.ModelSerializer):
    links = FooterLinkSerializer(many=True, read_only=True)
    
    class Meta:
        model = FooterColumn
        fields = ['id', 'title', 'order', 'is_active', 'links']


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


# About Page Serializers
class AboutStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutStatistic
        fields = ['id', 'number', 'label', 'order']


class AboutSectionSerializer(serializers.ModelSerializer):
    statistics = AboutStatisticSerializer(many=True, read_only=True)
    
    class Meta:
        model = AboutSection
        fields = ['id', 'section_type', 'label', 'heading', 'content', 'order', 'statistics']


class AboutImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutImage
        fields = '__all__'


class AboutHeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutHero
        fields = '__all__'


# Contact Form Serializer
class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']



# Widget System Serializers
class WidgetStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = WidgetStatistic
        fields = ['id', 'number', 'label', 'order']


class WidgetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WidgetImage
        fields = ['id', 'image', 'alt_text', 'caption', 'order']


class WidgetFAQItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WidgetFAQItem
        fields = ['id', 'question', 'answer', 'order']


class WidgetHeroBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WidgetHeroBanner
        fields = ['title', 'subtitle', 'background_image', 'overlay_opacity', 'text_color']


class WidgetTextSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WidgetTextSection
        fields = ['label', 'heading', 'content', 'text_align']


class WidgetHTMLContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WidgetHTMLContent
        fields = ['html_content', 'css_classes']


class WidgetDetailSerializer(serializers.ModelSerializer):
    # Content based on widget type
    hero_banner_content = WidgetHeroBannerSerializer(read_only=True)
    text_section_content = WidgetTextSectionSerializer(read_only=True)
    html_content = WidgetHTMLContentSerializer(read_only=True)
    statistics = WidgetStatisticSerializer(many=True, read_only=True)
    images = WidgetImageSerializer(many=True, read_only=True)
    faq_items = WidgetFAQItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Widget
        fields = [
            'id', 'name', 'widget_type', 'is_active',
            'hero_banner_content', 'text_section_content', 'html_content',
            'statistics', 'images', 'faq_items'
        ]


class PageWidgetSerializer(serializers.ModelSerializer):
    widget = WidgetDetailSerializer(read_only=True)
    
    class Meta:
        model = PageWidget
        fields = ['id', 'widget', 'order', 'is_active', 'config']


class PageSerializer(serializers.ModelSerializer):
    widgets = serializers.SerializerMethodField()
    
    class Meta:
        model = Page
        fields = ['id', 'title', 'slug', 'meta_description', 'is_active', 'widgets', 'created_at', 'updated_at']
    
    def get_widgets(self, obj):
        page_widgets = obj.page_widgets.filter(is_active=True).select_related('widget').order_by('order')
        return PageWidgetSerializer(page_widgets, many=True).data


class PageListSerializer(serializers.ModelSerializer):
    widget_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Page
        fields = ['id', 'title', 'slug', 'meta_description', 'is_active', 'widget_count']
    
    def get_widget_count(self, obj):
        return obj.page_widgets.filter(is_active=True).count()
