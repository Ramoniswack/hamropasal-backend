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
