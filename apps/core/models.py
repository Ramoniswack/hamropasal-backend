from django.db import models


class SiteSettings(models.Model):
    """Global site settings"""
    shipping_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=100.00,
        help_text="Default shipping cost in NPR"
    )
    free_shipping_threshold = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=5000.00,
        help_text="Order amount for free shipping in NPR"
    )
    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text="Tax rate in percentage"
    )
    currency_symbol = models.CharField(max_length=10, default='NPR')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        return "Site Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class AnalyticsProxy(models.Model):
    """Proxy model for Analytics Dashboard in admin sidebar"""
    class Meta:
        managed = False
        verbose_name = '📊 Analytics Dashboard'
        verbose_name_plural = '📊 Analytics Dashboard'
        app_label = 'core'



class NewsletterSubscriber(models.Model):
    """Newsletter subscription management"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    unsubscribe_token = models.CharField(max_length=64, unique=True, blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'
        ordering = ['-subscribed_at']

    def __str__(self):
        status = "Active" if self.is_active else "Unsubscribed"
        return f"{self.email} ({status})"

    def save(self, *args, **kwargs):
        if not self.unsubscribe_token:
            import uuid
            self.unsubscribe_token = uuid.uuid4().hex
        super().save(*args, **kwargs)
