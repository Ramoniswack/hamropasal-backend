from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.categories.models import Category


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    sku = models.CharField(max_length=100, blank=True, help_text="Stock Keeping Unit")
    
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    stock = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=10, help_text="Alert when stock falls below this number")
    
    # Sales tracking
    units_sold = models.PositiveIntegerField(default=0, editable=False)
    revenue_generated = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured']),
            models.Index(fields=['-units_sold']),  # For best sellers
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.sku:
            # Generate SKU from first 3 letters of name + random string
            import uuid
            self.sku = f"{self.name[:3].upper()}{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def is_low_stock(self):
        return 0 < self.stock <= self.low_stock_threshold

    @property
    def final_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def discount_percentage(self):
        if self.discount_price and self.discount_price < self.price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0

    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 2)
        return 0

    @property
    def review_count(self):
        """Count of approved reviews"""
        return self.reviews.filter(is_approved=True).count()

    def reduce_stock(self, quantity):
        """Reduce stock and create history entry"""
        if self.stock >= quantity:
            old_stock = self.stock
            self.stock -= quantity
            self.save()
            
            # Create stock history
            StockHistory.objects.create(
                product=self,
                change_type='sale',
                quantity_change=-quantity,
                stock_before=old_stock,
                stock_after=self.stock,
                notes=f"Stock reduced by {quantity} units due to sale"
            )
            return True
        return False

    def increase_stock(self, quantity, change_type='purchase', notes='', user=None):
        """Increase stock and create history entry"""
        old_stock = self.stock
        self.stock += quantity
        self.save()
        
        # Create stock history
        StockHistory.objects.create(
            product=self,
            change_type=change_type,
            quantity_change=quantity,
            stock_before=old_stock,
            stock_after=self.stock,
            notes=notes or f"Stock increased by {quantity} units",
            created_by=user
        )


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ['-is_primary', 'created_at']

    def __str__(self):
        return f"{self.product.name} - Image"

    def save(self, *args, **kwargs):
        # Ensure only one primary image per product
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)


class ProductTag(models.Model):
    """Tags for products (e.g., 'organic', 'gluten-free', 'vegan')"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Product Tag'
        verbose_name_plural = 'Product Tags'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductTagAssignment(models.Model):
    """Many-to-many relationship between products and tags"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='tag_assignments')
    tag = models.ForeignKey(ProductTag, on_delete=models.CASCADE, related_name='product_assignments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Product Tag Assignment'
        verbose_name_plural = 'Product Tag Assignments'
        unique_together = ['product', 'tag']

    def __str__(self):
        return f"{self.product.name} - {self.tag.name}"


class NutritionalFact(models.Model):
    """Nutritional information for products"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='nutritional_facts')
    protein_grams = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    protein_percentage = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    carbohydrates_grams = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    carbohydrates_percentage = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    fats_grams = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fats_percentage = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    calories = models.IntegerField(default=0)
    serving_size = models.CharField(max_length=100, blank=True)
    disclaimer = models.TextField(default="Percent Daily Values are based on a 2,000 calorie diet. Your Daily Values may be higher or lower depending on your calorie needs.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Nutritional Fact'
        verbose_name_plural = 'Nutritional Facts'

    def __str__(self):
        return f"Nutritional Facts for {self.product.name}"


class ProductFeature(models.Model):
    """Product features (e.g., '100% Natural', 'No chemicals', 'Secure payment')"""
    FEATURE_ICONS = [
        ('leaf', 'Leaf (Natural)'),
        ('flask', 'Flask (No Chemicals)'),
        ('credit-card', 'Credit Card (Secure Payment)'),
        ('headphones', 'Headphones (24/7 Support)'),
        ('truck', 'Truck (Fast Delivery)'),
        ('shield', 'Shield (Quality Guarantee)'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, choices=FEATURE_ICONS, default='leaf')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Product Feature'
        verbose_name_plural = 'Product Features'
        ordering = ['order', 'title']

    def __str__(self):
        return f"{self.product.name} - {self.title}"


class RelatedProduct(models.Model):
    """Related products for cross-selling"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='related_from')
    related_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='related_to')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Related Product'
        verbose_name_plural = 'Related Products'
        unique_together = ['product', 'related_product']
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} -> {self.related_product.name}"


class ProductReview(models.Model):
    """Customer reviews for products"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'
        ordering = ['-created_at']
        unique_together = ['product', 'user']  # One review per user per product
        indexes = [
            models.Index(fields=['product', 'is_approved']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"


class StockHistory(models.Model):
    """Track stock changes for inventory management"""
    CHANGE_TYPES = [
        ('purchase', 'Purchase Order'),
        ('sale', 'Sale'),
        ('return', 'Return'),
        ('adjustment', 'Manual Adjustment'),
        ('damaged', 'Damaged/Lost'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_history')
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPES)
    quantity_change = models.IntegerField()  # Positive for increase, negative for decrease
    stock_before = models.IntegerField()
    stock_after = models.IntegerField()
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Stock History'
        verbose_name_plural = 'Stock Histories'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.change_type} ({self.quantity_change:+d})"
