from django.db import models


class HeroBanner(models.Model):
    """Hero slider banners for homepage"""
    title = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(upload_to='banners/hero/')
    discount_percentage = models.IntegerField(default=50)
    discount_text = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_text = models.CharField(max_length=100)
    button_text = models.CharField(max_length=50, default="Shop Now")
    button_link = models.CharField(max_length=200, default="#")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Hero Banner'
        verbose_name_plural = 'Hero Banners'

    def __str__(self):
        return self.title[:50]


class MarketplaceBanner(models.Model):
    """Marketplace promotional banners"""
    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='banners/marketplace/')
    button_text = models.CharField(max_length=50, default="Shop Now")
    button_link = models.CharField(max_length=200, default="#")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Marketplace Banner'
        verbose_name_plural = 'Marketplace Banners'

    def __str__(self):
        return self.title[:50]


class PromoBanner(models.Model):
    """Single promo banner"""
    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='banners/promo/')
    button_text = models.CharField(max_length=50, default="Shop Now")
    button_link = models.CharField(max_length=200, default="#")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Promo Banner'
        verbose_name_plural = 'Promo Banners'

    def __str__(self):
        return self.title


class ScrollingBanner(models.Model):
    """Scrolling offer banner text"""
    text = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Scrolling Banner'
        verbose_name_plural = 'Scrolling Banners'

    def __str__(self):
        return self.text
