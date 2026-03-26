from django.core.management.base import BaseCommand
from apps.banners.models import HeroBanner, MarketplaceBanner, PromoBanner, ScrollingBanner
from apps.cms.models import Feature, Testimonial, FAQ


class Command(BaseCommand):
    help = 'Seeds homepage content (banners, features, testimonials, FAQs)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding homepage content...')
        
        # Clear existing data
        HeroBanner.objects.all().delete()
        MarketplaceBanner.objects.all().delete()
        PromoBanner.objects.all().delete()
        ScrollingBanner.objects.all().delete()
        Feature.objects.all().delete()
        Testimonial.objects.all().delete()
        FAQ.objects.all().delete()
        
        # Create Hero Banners
        self.stdout.write('Creating hero banners...')
        HeroBanner.objects.create(
            title='Curated marketplace collections built for quality everyday living.',
            description='<p>Carefully curated products from trusted sellers, designed to deliver quality, value, and a seamless shopping experience for everyday needs.</p>',
            image='banners/hero/hero-background.png',
            discount_percentage=50,
            discount_text='<p>Special discount for a limited number,<br>hurry and don\'t miss out.</p>',
            price='24.99',
            price_text='With prices<br>starting from',
            button_text='Shop Now',
            button_link='/shop',
            order=1,
            is_active=True
        )
        
        HeroBanner.objects.create(
            title='Smart marketplace essentials created for modern daily needs',
            description='<p>Discover quality products from verified sellers, offering exceptional value and convenience for your everyday lifestyle.</p>',
            image='banners/hero/slider-01-b.webp',
            discount_percentage=40,
            discount_text='<p>Limited time offer!<br>Shop now and save big.</p>',
            price='19.99',
            price_text='Starting at<br>just',
            button_text='Shop Now',
            button_link='/shop',
            order=2,
            is_active=True
        )
        
        # Create Marketplace Banners
        self.stdout.write('Creating marketplace banners...')
        MarketplaceBanner.objects.create(
            title='Smart Marketplace Products<br>for Quality-Conscious Buyers',
            description='<p>Shop smart with our carefully selected marketplace products. Find quality items that offer great value, durability, and practical functionality for your everyday needs.</p>',
            image='banners/marketplace/banner1card.webp',
            button_text='Shop Now',
            button_link='/shop',
            order=1,
            is_active=True
        )
        
        MarketplaceBanner.objects.create(
            title='Premium Curated Goods<br>for Modern Daily Living',
            description='<p>Discover premium marketplace products curated for modern living. Browse trusted sellers offering quality goods that enhance your daily routine and lifestyle.</p>',
            image='banners/marketplace/banner2card.webp',
            button_text='Shop Now',
            button_link='/shop',
            order=2,
            is_active=True
        )
        
        MarketplaceBanner.objects.create(
            title='Trusted Marketplace Items<br>for Essential Daily Needs',
            description='<p>Find reliable marketplace solutions for your daily essentials. Shop with confidence knowing every product is selected for quality, value, and customer satisfaction.</p>',
            image='banners/marketplace/banner3card.webp',
            button_text='Shop Now',
            button_link='/shop',
            order=3,
            is_active=True
        )
        
        # Create Promo Banner
        self.stdout.write('Creating promo banner...')
        PromoBanner.objects.create(
            title='Find Reliable Products<br>In One Marketplace',
            description='<p>Quality marketplace essentials for everyday use</p>',
            image='banners/promo/promobanner.webp',
            button_text='Shop Now',
            button_link='/shop',
            is_active=True
        )
        
        # Create Scrolling Banners
        self.stdout.write('Creating scrolling banners...')
        ScrollingBanner.objects.create(
            text='$50 OFF YOUR FIRST ORDER',
            is_active=True
        )
        
        ScrollingBanner.objects.create(
            text='FREE SHIPPING ON ORDERS OVER $100',
            is_active=True
        )
        
        # Create Features
        self.stdout.write('Creating features...')
        Feature.objects.create(
            title='Fast Shipping',
            description='<p>Receive your order anywhere in the world</p>',
            icon_name='fast-shipping',
            order=1,
            is_active=True
        )
        
        Feature.objects.create(
            title='Return Policy',
            description='<p>Talk to our experts by chat or e-mail</p>',
            icon_name='return-policy',
            order=2,
            is_active=True
        )
        
        Feature.objects.create(
            title='Payment Security',
            description='<p>Don\'t worry, all orders are processed securely</p>',
            icon_name='payment-security',
            order=3,
            is_active=True
        )
        
        Feature.objects.create(
            title='Free Shipping',
            description='<p>Collect points and enjoy a host of benefits!</p>',
            icon_name='free-shipping',
            order=4,
            is_active=True
        )
        
        # Create Testimonials
        self.stdout.write('Creating testimonials...')
        Testimonial.objects.create(
            author_name='Viktoria Blomqvist',
            author_role='Founder Blonwe Store',
            text='Outstanding marketplace experience! The quality of products exceeded my expectations. Fast shipping and excellent customer service made my shopping journey smooth and enjoyable.',
            rating=5,
            order=1,
            is_active=True
        )
        
        Testimonial.objects.create(
            author_name='Marcus Anderson',
            author_role='Business Owner',
            text='Amazing selection of products at competitive prices. The user interface is intuitive and makes finding what I need incredibly easy. Customer support team is responsive and helpful.',
            rating=5,
            order=2,
            is_active=True
        )
        
        Testimonial.objects.create(
            author_name='Sarah Mitchell',
            author_role='Marketing Director',
            text='Best marketplace platform I\'ve used in years. Product descriptions are accurate, delivery is prompt, and the return policy is fair. The variety of sellers ensures I always find what I\'m looking for.',
            rating=5,
            order=3,
            is_active=True
        )
        
        Testimonial.objects.create(
            author_name='David Chen',
            author_role='Tech Entrepreneur',
            text='Exceptional quality and service! Every purchase has been exactly as described. The checkout process is seamless, and I appreciate the secure payment options.',
            rating=5,
            order=4,
            is_active=True
        )
        
        # Create FAQs
        self.stdout.write('Creating FAQs...')
        FAQ.objects.create(
            question='How does our marketplace connect buyers with trusted sellers?',
            answer='<p>Our marketplace carefully vets all sellers through a rigorous verification process. We ensure that each seller meets our quality standards and has a proven track record of customer satisfaction. This creates a trusted environment where buyers can shop with confidence.</p>',
            order=1,
            is_active=True
        )
        
        FAQ.objects.create(
            question='What makes our marketplace products reliable and high quality?',
            answer='<p>We implement strict quality control measures including seller verification, customer reviews, and product inspections. Every item listed on our platform must meet our quality standards before being made available to customers.</p>',
            order=2,
            is_active=True
        )
        
        FAQ.objects.create(
            question='How are products selected before being listed on the marketplace?',
            answer='<p>Products undergo a thorough vetting process that includes quality checks, seller verification, compliance with marketplace standards, and review of product descriptions and images to ensure accuracy.</p>',
            order=3,
            is_active=True
        )
        
        FAQ.objects.create(
            question='Can I trust sellers and reviews on this marketplace platform?',
            answer='<p>Yes! We verify all sellers and implement a robust review system to ensure authenticity. Our team monitors reviews for suspicious activity and removes fake reviews to maintain trustworthiness.</p>',
            order=4,
            is_active=True
        )
        
        FAQ.objects.create(
            question='What payment methods are supported across marketplace vendors?',
            answer='<p>We support multiple secure payment methods including credit cards, debit cards, PayPal, and other trusted payment gateways. All transactions are encrypted and processed securely.</p>',
            order=5,
            is_active=True
        )
        
        FAQ.objects.create(
            question='How does shipping and delivery work with multiple sellers?',
            answer='<p>Each seller manages their own shipping, but we provide tracking and support to ensure smooth delivery. You\'ll receive tracking information for each order and can monitor delivery status in your account.</p>',
            order=6,
            is_active=True
        )
        
        FAQ.objects.create(
            question='What is the return and refund policy for marketplace orders?',
            answer='<p>We offer a flexible return policy. Items can be returned within 30 days for a full refund, subject to seller terms. Our customer support team is available to assist with any return or refund requests.</p>',
            order=7,
            is_active=True
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded homepage content!'))
        self.stdout.write(f'Created:')
        self.stdout.write(f'  - {HeroBanner.objects.count()} Hero Banners')
        self.stdout.write(f'  - {MarketplaceBanner.objects.count()} Marketplace Banners')
        self.stdout.write(f'  - {PromoBanner.objects.count()} Promo Banner')
        self.stdout.write(f'  - {ScrollingBanner.objects.count()} Scrolling Banners')
        self.stdout.write(f'  - {Feature.objects.count()} Features')
        self.stdout.write(f'  - {Testimonial.objects.count()} Testimonials')
        self.stdout.write(f'  - {FAQ.objects.count()} FAQs')
