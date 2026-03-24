from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.core.files import File
from pathlib import Path
import shutil
from apps.categories.models import Category
from apps.products.models import Product, ProductImage
from apps.banners.models import HeroBanner, MarketplaceBanner, PromoBanner, ScrollingBanner
from apps.cms.models import (
    Testimonial, FAQ, Feature, Vendor, SiteSettings,
    NavigationMenu, FooterColumn, FooterLink, Store
)


class Command(BaseCommand):
    help = 'Seed ALL database with complete ecommerce data using real images from frontend'

    def __init__(self):
        super().__init__()
        # Path to frontend public folder
        self.frontend_public = Path(__file__).resolve().parent.parent.parent.parent.parent.parent / 'frontend' / 'public'
        self.media_root = Path(__file__).resolve().parent.parent.parent.parent.parent / 'media'

    def handle(self, *args, **kwargs):
        self.stdout.write('[*] Starting comprehensive data seeding with real images...')
        self.stdout.write(f'[*] Frontend public folder: {self.frontend_public}')
        self.stdout.write(f'[*] Media root: {self.media_root}')
        
        # Check if frontend public folder exists
        if not self.frontend_public.exists():
            self.stdout.write(self.style.ERROR(f'[!] Frontend public folder not found: {self.frontend_public}'))
            self.stdout.write(self.style.WARNING('[!] Please ensure frontend folder is in the correct location'))
            return
        
        # Seed in order
        self.seed_site_settings()
        self.seed_navigation()
        self.seed_footer()
        self.seed_stores()
        self.seed_categories()
        self.seed_products_with_images()
        self.seed_hero_banners()
        self.seed_marketplace_banners()
        self.seed_promo_banner()
        self.seed_scrolling_banner()
        self.seed_features()
        self.seed_faqs()
        self.seed_testimonials()
        self.seed_vendors()
        
        self.stdout.write(self.style.SUCCESS('[OK] ALL DATA SEEDED SUCCESSFULLY WITH REAL IMAGES!'))
        self.stdout.write(self.style.SUCCESS('[DONE] Your backend is now 100% ready with real images!'))

    def copy_image(self, source_filename, destination_path, destination_filename=None):
        """Copy image from frontend/public to media folder"""
        try:
            source = self.frontend_public / source_filename
            
            if not source.exists():
                self.stdout.write(f'    [!] Image not found: {source_filename}')
                return None
            
            # Create destination directory if it doesn't exist
            dest_dir = self.media_root / destination_path
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            # Use original filename if not specified
            if destination_filename is None:
                destination_filename = source_filename
            
            destination = dest_dir / destination_filename
            
            # Copy the file
            shutil.copy2(source, destination)
            
            # Return the relative path for Django
            return f'{destination_path}/{destination_filename}'
            
        except Exception as e:
            self.stdout.write(f'    [!] Error copying image {source_filename}: {e}')
            return None

    def seed_site_settings(self):
        self.stdout.write('Seeding site settings...')
        settings, created = SiteSettings.objects.get_or_create(
            id=1,
            defaults={
                'site_name': 'Hamro Pasal',
                'top_banner_text': 'FREE delivery & 40% Discount for next 3 orders! Place your 1st Order in',
                'top_banner_bg_color': '#9ACD32',
                'show_top_banner': True,
                'phone_number': '+91 289 87 21',
                'phone_description': 'Contact us by calling the Helpline 24/7',
                'email': 'info@example.com',
                'address': '75 Hoel Trok Station Road, Cardiff, UK\nUnited Kingdom',
                'app_download_title': 'Download our app',
                'app_download_subtitle': 'Download App Get -10% Discount',
                'newsletter_title': 'Join the Supgor Club!',
                'newsletter_description': 'Whether you are welcoming new contacts or sharing the latest news, you can make your business look good in just a few clicks.',
                'copyright_text': 'Copyright 2026 Supgor WordPress Theme. All right reserved. Powered by KLBTheme.',
            }
        )
        
        # Add site logos from frontend
        if not settings.site_logo:
            logo_path = self.copy_image('logoecommerce.png', 'site', 'site-logo.png')
            if logo_path:
                settings.site_logo = logo_path
        
        if not settings.site_logo_footer:
            footer_logo_path = self.copy_image('logo-footer-41ef32.png', 'site', 'site-logo-footer.png')
            if footer_logo_path:
                settings.site_logo_footer = footer_logo_path
        
        settings.save()
        self.stdout.write('  [+] Site settings configured with real logos')


    def seed_navigation(self):
        self.stdout.write('Seeding navigation menu...')
        nav_items = [
            {'title': 'Home', 'url': '/', 'order': 1},
            {'title': 'Shop', 'url': '/shop', 'order': 2},
            {'title': 'Beverages', 'url': '/shop?category=Beverages', 'order': 3},
            {'title': 'Bakery', 'url': '/shop?category=Bakery', 'order': 4},
            {'title': 'Categories', 'url': '#', 'order': 5},
            {'title': 'Blog', 'url': '#', 'order': 6},
            {'title': 'Contact', 'url': '/contact', 'order': 7},
        ]
        
        for item in nav_items:
            NavigationMenu.objects.get_or_create(
                title=item['title'],
                defaults={'url': item['url'], 'order': item['order']}
            )
        self.stdout.write(f'  [+] Created {len(nav_items)} navigation items')

    def seed_footer(self):
        self.stdout.write('Seeding footer...')
        
        footer_data = [
            {
                'title': 'Get to Know Us',
                'links': [
                    'Careers for Supgor', 'About Supgor', 'Inverstor Relations',
                    'Supgor Devices', 'Customer reviews', 'Social Responsibility', 'Store Locations'
                ]
            },
            {
                'title': 'Let Us Help You',
                'links': [
                    'Your Orders', 'Returns & Replacements', 'Shipping Rates & Policies',
                    'Refund and Returns Policy', 'Privacy Policy', 'Terms and Conditions',
                    'Cookie Settings', 'Help Center'
                ]
            },
            {
                'title': 'Make Money with Us',
                'links': [
                    'Sell on Supgor', 'Sell Your Services on Supgor', 'Sell on Supgor Business',
                    'Sell Your Apps on Supgor', 'Become an Affilate', 'Advertise Your Products',
                    'Sell-Publish with Us', 'Become an Supgor Vendor'
                ]
            },
            {
                'title': 'For Buyers',
                'links': ['FAQ', 'Track Order', 'Contact', 'About Us']
            }
        ]
        
        for col_data in footer_data:
            column, _ = FooterColumn.objects.get_or_create(
                title=col_data['title'],
                defaults={'order': footer_data.index(col_data) + 1}
            )
            for link_title in col_data['links']:
                FooterLink.objects.get_or_create(
                    column=column,
                    title=link_title,
                    defaults={'url': '#', 'order': col_data['links'].index(link_title) + 1}
                )
        
        self.stdout.write(f'  [+] Created {len(footer_data)} footer columns')


    def seed_stores(self):
        self.stdout.write('Seeding store locations...')
        stores = [
            {
                'country': 'United States',
                'city': 'United States',
                'address': '205 Middle Road, 2nd Floor, New York\n2485',
                'phone': '+02 1234 567 88',
                'email': 'info@example.com',
                'order': 1
            },
            {
                'country': 'Netherlands',
                'city': 'Amsterdam',
                'address': '205 Middle Road, 2nd Floor, New York\n2485',
                'phone': '+02 1234 567 88',
                'email': 'info@example.com',
                'order': 2
            }
        ]
        
        for store in stores:
            Store.objects.get_or_create(
                city=store['city'],
                country=store['country'],
                defaults=store
            )
        
        self.stdout.write(f'  [+] Created {len(stores)} store locations')

    def seed_categories(self):
        self.stdout.write('Seeding categories...')
        categories_data = [
            ('Bakery', 'categ1.png'),
            ('Beverages', 'categ2.png'),
            ('Dairy & Eggs', 'categ3.png'),
            ('Deli', 'categ4.png'),
            ('Frozen Foods', 'categ5.png'),
            ('Fruits & Vegetables', 'categ6.png'),
            ('Healthcare', 'categ7.png'),
            ('Meat & Seafood', 'categ8.png'),
            ('Snacks', 'categ9.png'),
        ]
        
        categories_created = 0
        for cat_name, image_file in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name), 'is_active': True}
            )
            
            if created:
                categories_created += 1
            
            # Add category image from frontend
            if not category.image:
                image_path = self.copy_image(image_file, 'categories', f'{category.slug}.png')
                if image_path:
                    category.image = image_path
                    category.save()
        
        self.stdout.write(f'  [+] Created {categories_created} categories with real images')


    def seed_products_with_images(self):
        self.stdout.write('Seeding products with real images...')
        
        # Get categories
        bakery = Category.objects.get(name='Bakery')
        beverages = Category.objects.get(name='Beverages')
        fruits = Category.objects.get(name='Fruits & Vegetables')
        meat = Category.objects.get(name='Meat & Seafood')
        dairy = Category.objects.get(name='Dairy & Eggs')
        
        # Product images mapping (product name -> [image files])
        product_images = {
            'product1': ['product1image.webp', 'product-thumb-1-76eae0.png', 'product-main-image-56586a.png'],
            'product2': ['product2image.webp', 'product-thumb-2-76eae0.png', 'product-ritz-crackers-56586a.png'],
            'product3': ['product3image.webp', 'product-thumb-3-76eae0.png', 'product-lettuce-56586a.png'],
            'product4': ['product4image.webp', 'product-chicken-nuggets-56586a.png', 'product-pumpkin-cookies-56586a.png'],
            'product5': ['product5image.webp', 'product-honey-ointment-56586a.png', 'product-main-image-56586a.png'],
        }
        
        products_data = [
            # Bakery (6 products)
            {'name': 'Artisan Sourdough Bread Loaf', 'category': bakery, 'price': 7.80, 'discount_price': 4.99, 'stock': 28, 'short_desc': 'Fresh artisan sourdough bread', 'images': 'product1'},
            {'name': 'Fresh Croissants Pack of 6', 'category': bakery, 'price': 12.25, 'discount_price': 6.99, 'stock': 15, 'short_desc': 'Buttery fresh croissants', 'images': 'product2'},
            {'name': 'Whole Grain Dinner Rolls', 'category': bakery, 'price': 7.25, 'discount_price': 3.49, 'stock': 42, 'short_desc': 'Healthy whole grain rolls', 'images': 'product3'},
            {'name': 'Chocolate Chip Muffins 4-Pack', 'category': bakery, 'price': 10.15, 'discount_price': 5.99, 'stock': 33, 'short_desc': 'Delicious chocolate chip muffins', 'images': 'product4'},
            {'name': 'Cinnamon Swirl Coffee Cake', 'category': bakery, 'price': 14.50, 'discount_price': 8.99, 'stock': 12, 'short_desc': 'Sweet cinnamon coffee cake', 'images': 'product5'},
            {'name': 'Honey Wheat Sandwich Bread', 'category': bakery, 'price': 9.99, 'discount_price': 5.49, 'stock': 18, 'short_desc': 'Soft honey wheat bread', 'images': 'product1'},
            
            # Beverages (6 products)
            {'name': 'Fresh Orange Juice 1L', 'category': beverages, 'price': 5.32, 'discount_price': 3.99, 'stock': 45, 'short_desc': '100% fresh orange juice', 'images': 'product2'},
            {'name': 'Premium Coffee Beans 500g', 'category': beverages, 'price': 18.56, 'discount_price': 12.99, 'stock': 22, 'short_desc': 'Premium arabica coffee beans', 'images': 'product3'},
            {'name': 'Sparkling Water 6-Pack', 'category': beverages, 'price': 5.61, 'discount_price': 4.49, 'stock': 38, 'short_desc': 'Refreshing sparkling water', 'images': 'product4'},
            {'name': 'Green Tea Variety Pack', 'category': beverages, 'price': 13.83, 'discount_price': 8.99, 'stock': 16, 'short_desc': 'Assorted green tea flavors', 'images': 'product5'},
            {'name': 'Energy Drink 4-Pack', 'category': beverages, 'price': 11.10, 'discount_price': 7.99, 'stock': 31, 'short_desc': 'Boost your energy', 'images': 'product1'},
            {'name': 'Coconut Water 12-Pack', 'category': beverages, 'price': 26.65, 'discount_price': 15.99, 'stock': 24, 'short_desc': 'Natural coconut water', 'images': 'product2'},
            
            # Fruits & Vegetables (6 products)
            {'name': 'Organic Banana Bunch', 'category': fruits, 'price': 3.52, 'discount_price': 2.99, 'stock': 67, 'short_desc': 'Fresh organic bananas', 'images': 'product3'},
            {'name': 'Fresh Strawberries 500g', 'category': fruits, 'price': 7.68, 'discount_price': 5.99, 'stock': 43, 'short_desc': 'Sweet fresh strawberries', 'images': 'product4'},
            {'name': 'Mixed Salad Greens 300g', 'category': fruits, 'price': 4.26, 'discount_price': 3.49, 'stock': 52, 'short_desc': 'Fresh mixed salad greens', 'images': 'product5'},
            {'name': 'Organic Carrots 1kg', 'category': fruits, 'price': 3.32, 'discount_price': 2.49, 'stock': 38, 'short_desc': 'Organic fresh carrots', 'images': 'product1'},
            {'name': 'Fresh Avocados 4-Pack', 'category': fruits, 'price': 9.99, 'discount_price': 6.99, 'stock': 29, 'short_desc': 'Ripe fresh avocados', 'images': 'product2'},
            {'name': 'Bell Peppers Mix 3-Pack', 'category': fruits, 'price': 6.24, 'discount_price': 4.99, 'stock': 35, 'short_desc': 'Colorful bell peppers', 'images': 'product3'},
            
            # Meat & Seafood (6 products)
            {'name': 'Fresh Salmon Fillet 500g', 'category': meat, 'price': 29.22, 'discount_price': 18.99, 'stock': 14, 'short_desc': 'Premium salmon fillet', 'images': 'product4'},
            {'name': 'Premium Beef Steak 400g', 'category': meat, 'price': 34.71, 'discount_price': 24.99, 'stock': 8, 'short_desc': 'Premium quality beef steak', 'images': 'product5'},
            {'name': 'Chicken Breast 1kg', 'category': meat, 'price': 19.10, 'discount_price': 12.99, 'stock': 22, 'short_desc': 'Fresh chicken breast', 'images': 'product1'},
            {'name': 'Fresh Shrimp 300g', 'category': meat, 'price': 26.65, 'discount_price': 15.99, 'stock': 11, 'short_desc': 'Fresh premium shrimp', 'images': 'product2'},
            {'name': 'Ground Turkey 500g', 'category': meat, 'price': 11.99, 'discount_price': 8.99, 'stock': 19, 'short_desc': 'Lean ground turkey', 'images': 'product3'},
            {'name': 'Fresh Cod Fillet 400g', 'category': meat, 'price': 24.27, 'discount_price': 16.99, 'stock': 16, 'short_desc': 'Fresh cod fillet', 'images': 'product4'},
            
            # Dairy & Eggs (4 products)
            {'name': 'Organic Whole Milk 1 Gallon', 'category': dairy, 'price': 6.50, 'discount_price': 4.99, 'stock': 35, 'short_desc': 'Fresh organic milk', 'images': 'product5'},
            {'name': 'Free Range Eggs Dozen', 'category': dairy, 'price': 7.20, 'discount_price': 5.49, 'stock': 42, 'short_desc': 'Farm fresh eggs', 'images': 'product1'},
            {'name': 'Greek Yogurt 32oz', 'category': dairy, 'price': 9.50, 'discount_price': 6.99, 'stock': 28, 'short_desc': 'Creamy Greek yogurt', 'images': 'product2'},
            {'name': 'Cheddar Cheese Block 16oz', 'category': dairy, 'price': 10.99, 'discount_price': 7.49, 'stock': 19, 'short_desc': 'Sharp cheddar cheese', 'images': 'product3'},
        ]
        
        products_created = 0
        images_created = 0
        
        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'slug': slugify(prod_data['name']),
                    'category': prod_data['category'],
                    'price': prod_data['price'],
                    'discount_price': prod_data['discount_price'],
                    'stock': prod_data['stock'],
                    'is_featured': True,
                    'short_description': prod_data['short_desc'],
                    'description': f"High quality {prod_data['name']}. {prod_data['short_desc']}. Perfect for your daily needs. Fresh and carefully selected products.",
                    'is_active': True
                }
            )
            
            if created:
                products_created += 1
            
            # Create product images from frontend
            if not product.images.exists():
                image_key = prod_data['images']
                image_files = product_images.get(image_key, [])
                
                for idx, image_file in enumerate(image_files):
                    image_path = self.copy_image(image_file, 'products', f'{product.slug}-{idx+1}.{image_file.split(".")[-1]}')
                    if image_path:
                        ProductImage.objects.create(
                            product=product,
                            image=image_path,
                            is_primary=(idx == 0)
                        )
                        images_created += 1
        
        self.stdout.write(f'  [+] Created {products_created} products with {images_created} real images')


    def seed_hero_banners(self):
        self.stdout.write('Seeding hero banners...')
        banners = [
            {
                'title': 'Curated marketplace collections built for quality everyday living.',
                'description': 'Carefully curated products from trusted sellers, designed to deliver quality, value, and a seamless shopping experience for everyday needs.',
                'discount_percentage': 50,
                'discount_text': 'Special discount for a limited number, hurry and do not miss out.',
                'price': 24.99,
                'price_text': 'With prices starting from',
                'order': 1,
                'image': 'slider-01-b.webp'
            },
            {
                'title': 'Smart marketplace essentials created for modern daily needs',
                'description': 'Carefully curated products from trusted sellers, designed to deliver quality, value, and a seamless shopping experience for everyday needs.',
                'discount_percentage': 50,
                'discount_text': 'Special discount for a limited number, hurry and do not miss out.',
                'price': 24.99,
                'price_text': 'With prices starting from',
                'order': 2,
                'image': 'hero-background.png'
            }
        ]
        
        banners_created = 0
        for banner_data in banners:
            image_file = banner_data.pop('image')
            banner, created = HeroBanner.objects.get_or_create(
                title=banner_data['title'],
                defaults=banner_data
            )
            
            if created:
                banners_created += 1
            
            # Add banner image from frontend
            if not banner.image:
                image_path = self.copy_image(image_file, 'banners/hero', f'hero-banner-{banner.order}.{image_file.split(".")[-1]}')
                if image_path:
                    banner.image = image_path
                    banner.save()
        
        self.stdout.write(f'  [+] Created {banners_created} hero banners with real images')

    def seed_marketplace_banners(self):
        self.stdout.write('Seeding marketplace banners...')
        banners = [
            {
                'title': 'Smart Marketplace Products for Quality-Conscious Buyers',
                'description': 'Shop smart with our carefully selected marketplace products. Find quality items that offer great value, durability, and practical functionality for your everyday needs.',
                'order': 1,
                'image': 'banner1card.webp'
            },
            {
                'title': 'Premium Curated Goods for Modern Daily Living',
                'description': 'Discover premium marketplace products curated for modern living. Browse trusted sellers offering quality goods that enhance your daily routine and lifestyle.',
                'order': 2,
                'image': 'banner2card.webp'
            },
            {
                'title': 'Trusted Marketplace Items for Essential Daily Needs',
                'description': 'Find reliable marketplace solutions for your daily essentials. Shop with confidence knowing every product is selected for quality, value, and customer satisfaction.',
                'order': 3,
                'image': 'banner3card.webp'
            }
        ]
        
        banners_created = 0
        for banner_data in banners:
            image_file = banner_data.pop('image')
            banner, created = MarketplaceBanner.objects.get_or_create(
                title=banner_data['title'],
                defaults=banner_data
            )
            
            if created:
                banners_created += 1
            
            # Add banner image from frontend
            if not banner.image:
                image_path = self.copy_image(image_file, 'banners/marketplace', f'marketplace-banner-{banner.order}.webp')
                if image_path:
                    banner.image = image_path
                    banner.save()
        
        self.stdout.write(f'  [+] Created {banners_created} marketplace banners with real images')


    def seed_promo_banner(self):
        self.stdout.write('Seeding promo banner...')
        promo, created = PromoBanner.objects.get_or_create(
            title='Find Reliable Products In One Marketplace',
            defaults={
                'description': 'Quality marketplace essentials for everyday use',
                'button_text': 'Shop Now',
                'button_link': '/shop'
            }
        )
        
        # Add promo banner image from frontend
        if not promo.image:
            image_path = self.copy_image('promobanner.webp', 'banners/promo', 'promo-banner.webp')
            if image_path:
                promo.image = image_path
                promo.save()
        
        self.stdout.write('  [+] Created promo banner with real image')

    def seed_scrolling_banner(self):
        self.stdout.write('Seeding scrolling banner...')
        ScrollingBanner.objects.get_or_create(
            text='$50 OFF YOUR FIRST ORDER'
        )
        self.stdout.write('  [+] Created scrolling banner')

    def seed_features(self):
        self.stdout.write('Seeding features...')
        features = [
            {
                'title': 'Fast Shipping',
                'description': 'Receive your order anywhere in the world',
                'icon_name': 'fast-shipping',
                'order': 1
            },
            {
                'title': 'Return Policy',
                'description': 'Talk to our experts by chat or e-mail',
                'icon_name': 'return-policy',
                'order': 2
            },
            {
                'title': 'Payment Security',
                'description': 'Do not worry, all orders are processed securely',
                'icon_name': 'payment-security',
                'order': 3
            },
            {
                'title': 'Free Shipping',
                'description': 'Collect points and enjoy a host of benefits!',
                'icon_name': 'free-shipping',
                'order': 4
            }
        ]
        
        for feature in features:
            Feature.objects.get_or_create(
                title=feature['title'],
                defaults=feature
            )
        
        self.stdout.write(f'  [+] Created {len(features)} features')


    def seed_faqs(self):
        self.stdout.write('Seeding FAQs...')
        faqs = [
            {
                'question': 'How does our marketplace connect buyers with trusted sellers?',
                'answer': 'This is the first item accordion body. It is shown by default, until the collapse plugin adds the appropriate classes that we use to style each element. These classes control the overall appearance, as well as the showing and hiding via CSS transitions.',
                'order': 1
            },
            {
                'question': 'What makes our marketplace products reliable and high quality?',
                'answer': 'Our marketplace ensures product quality through rigorous seller verification, customer reviews, and quality control measures.',
                'order': 2
            },
            {
                'question': 'How are products selected before being listed on the marketplace?',
                'answer': 'Products undergo a thorough vetting process including quality checks, seller verification, and compliance with marketplace standards.',
                'order': 3
            },
            {
                'question': 'Can I trust sellers and reviews on this marketplace platform?',
                'answer': 'Yes, we verify all sellers and implement a robust review system to ensure authenticity and trustworthiness.',
                'order': 4
            },
            {
                'question': 'What payment methods are supported across marketplace vendors?',
                'answer': 'We support multiple payment methods including credit cards, debit cards, PayPal, and other secure payment gateways.',
                'order': 5
            },
            {
                'question': 'How does shipping and delivery work with multiple sellers?',
                'answer': 'Each seller manages their own shipping, but we provide tracking and support to ensure smooth delivery across all orders.',
                'order': 6
            },
            {
                'question': 'What is the return and refund policy for marketplace orders?',
                'answer': 'We offer a flexible return policy. Items can be returned within 30 days for a full refund, subject to seller terms.',
                'order': 7
            }
        ]
        
        for faq in faqs:
            FAQ.objects.get_or_create(
                question=faq['question'],
                defaults={'answer': faq['answer'], 'order': faq['order']}
            )
        
        self.stdout.write(f'  [+] Created {len(faqs)} FAQs')


    def seed_testimonials(self):
        self.stdout.write('Seeding testimonials...')
        testimonials = [
            {
                'author_name': 'Viktoria Blomqvist',
                'author_role': 'Founder Blonwe Store',
                'rating': 5,
                'text': 'Nysk dir retonas an teranera vel inte Adwords, sakasamma. Kaledes geologi fasam. Dogt reritoska mirad lalasade. Pol pona tusk kivening. Benest euserad preras metadata bespemyn.',
                'order': 1
            },
            {
                'author_name': 'Marcus Anderson',
                'author_role': 'Business Owner',
                'rating': 5,
                'text': 'Outstanding marketplace experience! The quality of products exceeded my expectations. Fast shipping and excellent customer service made my shopping journey smooth and enjoyable.',
                'order': 2
            },
            {
                'author_name': 'Sarah Mitchell',
                'author_role': 'Marketing Director',
                'rating': 5,
                'text': 'Amazing selection of products at competitive prices. The user interface is intuitive and makes finding what I need incredibly easy. Customer support team is responsive and helpful.',
                'order': 3
            },
            {
                'author_name': 'David Chen',
                'author_role': 'Tech Entrepreneur',
                'rating': 5,
                'text': 'Best marketplace platform I have used in years. Product descriptions are accurate, delivery is prompt, and the return policy is fair.',
                'order': 4
            },
            {
                'author_name': 'Emma Rodriguez',
                'author_role': 'Creative Designer',
                'rating': 5,
                'text': 'Exceptional quality and service! Every purchase has been exactly as described. The checkout process is seamless, and I appreciate the secure payment options.',
                'order': 5
            },
            {
                'author_name': 'James Thompson',
                'author_role': 'Retail Manager',
                'rating': 5,
                'text': 'Fantastic marketplace with trustworthy sellers. Product quality is consistently high, and prices are very competitive. Absolutely satisfied!',
                'order': 6
            }
        ]
        
        for testimonial in testimonials:
            Testimonial.objects.get_or_create(
                author_name=testimonial['author_name'],
                defaults=testimonial
            )
        
        self.stdout.write(f'  [+] Created {len(testimonials)} testimonials')


    def seed_vendors(self):
        self.stdout.write('Seeding vendors...')
        vendors = [
            {
                'name': 'Blonwe',
                'description': 'Premium marketplace vendor offering quality products with fast shipping and excellent customer service for everyday needs.',
                'rating': 4.17,
                'review_count': 12000,
                'review_text': 'Verified Reviews',
                'image': 'logoecommerce.png'
            },
            {
                'name': 'Grogin',
                'description': 'Trusted grocery marketplace specializing in organic foods, beverages, and healthy lifestyle products with competitive pricing.',
                'rating': 3.33,
                'review_count': 15000,
                'review_text': 'Customer Reviews',
                'image': 'logo-footer-41ef32.png'
            }
        ]
        
        vendors_created = 0
        for vendor_data in vendors:
            image_file = vendor_data.pop('image')
            vendor, created = Vendor.objects.get_or_create(
                name=vendor_data['name'],
                defaults=vendor_data
            )
            
            if created:
                vendors_created += 1
            
            # Add vendor logo from frontend
            if not vendor.logo:
                image_path = self.copy_image(image_file, 'vendors', f'{slugify(vendor.name)}-logo.png')
                if image_path:
                    vendor.logo = image_path
                    vendor.save()
        
        self.stdout.write(f'  [+] Created {vendors_created} vendors with real logos')
