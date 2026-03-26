from django.db import models
from ckeditor.fields import RichTextField


class SiteSettings(models.Model):
    """Global site settings"""
    site_name = models.CharField(max_length=200, default="Hamro Pasal")
    site_logo = models.ImageField(upload_to='site/', blank=True, null=True)
    site_logo_footer = models.ImageField(upload_to='site/', blank=True, null=True)
    
    # Header Settings
    top_banner_text = models.CharField(max_length=500, default="FREE delivery & 40% Discount for next 3 orders!")
    top_banner_bg_color = models.CharField(max_length=20, default="#9ACD32")
    show_top_banner = models.BooleanField(default=True)
    
    # Contact Information
    phone_number = models.CharField(max_length=50, default="+91 289 87 21")
    phone_description = models.CharField(max_length=200, default="Contact us by calling the Helpline 24/7")
    email = models.EmailField(default="info@example.com")
    address = models.TextField(default="75 Hoel Trok Station Road, Cardiff, UK")
    
    # App Download
    app_download_title = models.CharField(max_length=200, default="Download our app")
    app_download_subtitle = models.CharField(max_length=200, default="Download App Get -10% Discount")
    app_store_link = models.URLField(blank=True)
    google_play_link = models.URLField(blank=True)
    
    # Newsletter
    newsletter_title = models.CharField(max_length=200, default="Join the Supgor Club!")
    newsletter_description = RichTextField(default="Whether you're welcoming new contacts or sharing the latest news...", config_name='basic')
    
    # Copyright
    copyright_text = models.CharField(max_length=500, default="Copyright 2026 © Supgor WordPress Theme")
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '🔗 Header - Site Settings'
        verbose_name_plural = '🔗 Header - Site Settings'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError('There can only be one SiteSettings instance')
        return super().save(*args, **kwargs)


class NavigationMenu(models.Model):
    """Header navigation menu items"""
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, help_text="URL path (e.g., '/about', '/shop', '/contact')")
    custom_path = models.CharField(max_length=200, blank=True, help_text="Optional: Custom redirect path")
    open_in_new_tab = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = '🔗 Header - Navigation Menu'
        verbose_name_plural = '🔗 Header - Navigation Menus'

    def __str__(self):
        return self.title
    
    def get_url(self):
        """Return custom path if set, otherwise return url"""
        return self.custom_path if self.custom_path else self.url


class FooterColumn(models.Model):
    """Footer columns with links"""
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = '📑 Footer - Column'
        verbose_name_plural = '📑 Footer - Columns'

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    """Links within footer columns"""
    column = models.ForeignKey(FooterColumn, on_delete=models.CASCADE, related_name='links')
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200, help_text="URL path (e.g., '/about', '/faq', '/contact')")
    custom_path = models.CharField(max_length=200, blank=True, help_text="Optional: Custom redirect path")
    open_in_new_tab = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = '📑 Footer - Link'
        verbose_name_plural = '📑 Footer - Links'

    def __str__(self):
        return f"{self.column.title} - {self.title}"
    
    def get_url(self):
        """Return custom path if set, otherwise return url"""
        return self.custom_path if self.custom_path else self.url


class Store(models.Model):
    """Physical store locations"""
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'

    def __str__(self):
        return f"{self.city}, {self.country}"


class Testimonial(models.Model):
    """Customer testimonials"""
    author_name = models.CharField(max_length=200)
    author_role = models.CharField(max_length=200)
    rating = models.IntegerField(default=5)
    text = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f"{self.author_name} - {self.rating} stars"


class FAQ(models.Model):
    """Frequently Asked Questions"""
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question[:100]


class Feature(models.Model):
    """Site features (shipping, payment, etc.)"""
    title = models.CharField(max_length=200)
    description = RichTextField(config_name='basic')
    icon_name = models.CharField(max_length=100, help_text="Icon identifier (e.g., 'fast-shipping')")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Feature'
        verbose_name_plural = 'Features'

    def __str__(self):
        return self.title


class Vendor(models.Model):
    """Marketplace vendors"""
    name = models.CharField(max_length=200)
    description = RichTextField(config_name='basic')
    logo = models.ImageField(upload_to='vendors/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    review_count = models.IntegerField(default=0)
    review_text = models.CharField(max_length=100, default="Verified Reviews")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'

    def __str__(self):
        return self.name


# About Page Models
class AboutHero(models.Model):
    """About page hero section"""
    title = models.CharField(max_length=200, default="About Us")
    subtitle = models.TextField(default="To build a framework that makes auto repair predictable.")
    background_image = models.ImageField(upload_to='about/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'About Hero'
        verbose_name_plural = 'About Hero'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk and AboutHero.objects.exists():
            raise ValueError('There can only be one AboutHero instance')
        return super().save(*args, **kwargs)


class AboutSection(models.Model):
    """About page content sections"""
    SECTION_TYPE_CHOICES = [
        ('our_story', 'Our Story'),
        ('text_section', 'Text Section'),
        ('text_with_stats', 'Text with Statistics'),
    ]
    
    section_type = models.CharField(max_length=20, choices=SECTION_TYPE_CHOICES)
    label = models.CharField(max_length=100, blank=True, help_text="Small label above heading (e.g., 'OUR STORY')")
    heading = models.CharField(max_length=500)
    content = RichTextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'About Section'
        verbose_name_plural = 'About Sections'

    def __str__(self):
        return f"{self.get_section_type_display()} - {self.heading[:50]}"


class AboutStatistic(models.Model):
    """Statistics for about page"""
    section = models.ForeignKey(AboutSection, on_delete=models.CASCADE, related_name='statistics')
    number = models.CharField(max_length=20, help_text="e.g., '25K+', '57K+'")
    label = models.CharField(max_length=100, help_text="e.g., 'Happy Customers'")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'About Statistic'
        verbose_name_plural = 'About Statistics'

    def __str__(self):
        return f"{self.number} - {self.label}"


class AboutImage(models.Model):
    """Images for about page"""
    image = models.ImageField(upload_to='about/')
    alt_text = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'About Image'
        verbose_name_plural = 'About Images'

    def __str__(self):
        return self.alt_text


# Contact Form Model
class ContactSubmission(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'

    def __str__(self):
        return f"{self.name} - {self.subject[:30]}"


# Widget-Based Page Builder System
class Page(models.Model):
    """Dynamic pages that can be built using widgets"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    meta_description = models.TextField(blank=True, help_text="SEO meta description")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = '📄 Page Builder - Page'
        verbose_name_plural = '📄 Page Builder - Pages'

    def __str__(self):
        return self.title


class Widget(models.Model):
    """Reusable content widgets that can be added to pages"""
    WIDGET_TYPE_CHOICES = [
        # Hero/Banner Widgets
        ('hero_banner', 'Hero Banner'),
        ('image_banner', 'Image Banner'),
        
        # Text Content Widgets
        ('text_section', 'Text Section'),
        ('text_with_label', 'Text with Label (Our Story style)'),
        ('text_with_stats', 'Text with Statistics'),
        
        # Image Widgets
        ('single_image', 'Single Image'),
        ('two_column_images', 'Two Column Images'),
        ('image_gallery', 'Image Gallery'),
        
        # Feature Widgets
        ('features_grid', 'Features Grid'),
        ('testimonials_slider', 'Testimonials Slider'),
        ('vendors_showcase', 'Vendors Showcase'),
        
        # Interactive Widgets
        ('faq_accordion', 'FAQ Accordion'),
        ('contact_form', 'Contact Form'),
        ('store_locations', 'Store Locations'),
        
        # Product Widgets
        ('featured_products', 'Featured Products'),
        ('product_categories', 'Product Categories'),
        ('product_slider', 'Product Slider'),
        
        # Custom Widgets
        ('html_content', 'Custom HTML Content'),
        ('spacer', 'Spacer/Divider'),
    ]
    
    name = models.CharField(max_length=200, help_text="Internal name for this widget")
    widget_type = models.CharField(max_length=50, choices=WIDGET_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = '🧩 Page Builder - Widget'
        verbose_name_plural = '🧩 Page Builder - Widgets'

    def __str__(self):
        return f"{self.name} ({self.get_widget_type_display()})"


class PageWidget(models.Model):
    """Junction table linking widgets to pages with ordering"""
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='page_widgets')
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE, related_name='widget_pages')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Widget-specific configuration (JSON field for flexibility)
    config = models.JSONField(default=dict, blank=True, help_text="Widget-specific configuration")

    class Meta:
        ordering = ['order']
        unique_together = ['page', 'widget', 'order']
        verbose_name = '🧩 Page Builder - Page Widget'
        verbose_name_plural = '🧩 Page Builder - Page Widgets'

    def __str__(self):
        return f"{self.page.title} - {self.widget.name} (Order: {self.order})"


# Widget Content Models
class WidgetHeroBanner(models.Model):
    """Hero banner widget content"""
    widget = models.OneToOneField(Widget, on_delete=models.CASCADE, related_name='hero_banner_content')
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True)
    background_image = models.ImageField(upload_to='widgets/hero/')
    overlay_opacity = models.IntegerField(default=30, help_text="0-100")
    text_color = models.CharField(max_length=20, default='#FFFFFF')

    class Meta:
        verbose_name = '🧩 Page Builder - Hero Banner Content'
        verbose_name_plural = '🧩 Page Builder - Hero Banner Contents'

    def __str__(self):
        return self.title


class WidgetTextSection(models.Model):
    """Text section widget content"""
    widget = models.OneToOneField(Widget, on_delete=models.CASCADE, related_name='text_section_content')
    label = models.CharField(max_length=100, blank=True, help_text="Small label above heading")
    heading = models.CharField(max_length=500, blank=True)
    content = RichTextField()
    text_align = models.CharField(max_length=20, default='left', choices=[
        ('left', 'Left'),
        ('center', 'Center'),
        ('right', 'Right')
    ])

    class Meta:
        verbose_name = '🧩 Page Builder - Text Section Content'
        verbose_name_plural = '🧩 Page Builder - Text Section Contents'

    def __str__(self):
        return self.heading or self.label or 'Text Section'


class WidgetStatistic(models.Model):
    """Statistics for text with stats widget"""
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE, related_name='statistics')
    number = models.CharField(max_length=20, help_text="e.g., '25K+', '57K+'")
    label = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = '🧩 Page Builder - Widget Statistic'
        verbose_name_plural = '🧩 Page Builder - Widget Statistics'

    def __str__(self):
        return f"{self.number} - {self.label}"


class WidgetImage(models.Model):
    """Images for image widgets"""
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='widgets/images/')
    alt_text = models.CharField(max_length=200)
    caption = models.CharField(max_length=300, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = '🧩 Page Builder - Widget Image'
        verbose_name_plural = '🧩 Page Builder - Widget Images'

    def __str__(self):
        return self.alt_text


class WidgetFAQItem(models.Model):
    """FAQ items for FAQ accordion widget"""
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE, related_name='faq_items')
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = '🧩 Page Builder - Widget FAQ Item'
        verbose_name_plural = '🧩 Page Builder - Widget FAQ Items'

    def __str__(self):
        return self.question[:100]


class WidgetHTMLContent(models.Model):
    """Custom HTML content widget"""
    widget = models.OneToOneField(Widget, on_delete=models.CASCADE, related_name='html_content')
    html_content = RichTextField(help_text="Custom HTML content")
    css_classes = models.CharField(max_length=200, blank=True, help_text="Additional CSS classes")

    class Meta:
        verbose_name = '🧩 Page Builder - HTML Content'
        verbose_name_plural = '🧩 Page Builder - HTML Contents'

    def __str__(self):
        return f"HTML Content for {self.widget.name}"
