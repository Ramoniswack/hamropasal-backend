from django.core.management.base import BaseCommand
from apps.cms.models import (
    Page, Widget, PageWidget, WidgetHeroBanner, WidgetTextSection,
    WidgetStatistic, WidgetImage, WidgetFAQItem, WidgetHTMLContent,
    NavigationMenu, WidgetDynamicHero, WidgetProductSection
)
from apps.products.models import Product


class Command(BaseCommand):
    help = 'Seed a test page with various widgets including new Dynamic Hero and Product Section'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Starting enhanced page builder seeding...'))
        
        # Create or get the test page
        page, created = Page.objects.get_or_create(
            slug='our-story',
            defaults={
                'title': 'Our Story',
                'meta_description': 'Learn about our journey and what makes us special',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ Created page: {page.title}'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️  Page already exists: {page.title}'))
            # Clear existing widgets for fresh start
            page.page_widgets.all().delete()
            self.stdout.write(self.style.SUCCESS('🗑️  Cleared existing widgets'))
        
        # 1. Dynamic Hero Banner Widget (NEW!)
        hero_widget, _ = Widget.objects.get_or_create(
            name='Our Story Dynamic Hero',
            defaults={
                'widget_type': 'dynamic_hero',
                'is_active': True
            }
        )
        
        # Create WidgetDynamicHero content
        WidgetDynamicHero.objects.get_or_create(
            widget=hero_widget,
            defaults={
                'title': 'Our Journey to Excellence',
                'description': '<p>Building a marketplace that connects quality products with conscious consumers since 2020</p>',
                'show_discount_badge': False,
                'show_button': True,
                'button_text': 'Explore Our Products',
                'button_link': '/shop',
                'show_price': False,
                'text_color': '#FFFFFF',
                'overlay_opacity': 40,
            }
        )
        
        PageWidget.objects.create(
            page=page,
            widget=hero_widget,
            order=1,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('✅ Added Dynamic Hero Banner widget'))
        
        # 2. Text Section Widget - Introduction
        intro_widget, _ = Widget.objects.get_or_create(
            name='Story Introduction',
            defaults={
                'widget_type': 'text_section',
                'is_active': True
            }
        )
        
        WidgetTextSection.objects.get_or_create(
            widget=intro_widget,
            defaults={
                'heading': 'Welcome to Our Marketplace',
                'content': '''<p>Founded in 2020, we started with a simple mission: to create a platform where quality meets convenience. 
                Our marketplace brings together the best vendors and products, carefully curated to ensure you get nothing but the best.</p>
                <p>We believe in transparency, quality, and exceptional customer service. Every product on our platform goes through 
                rigorous quality checks, and every vendor is vetted to ensure they meet our high standards.</p>''',
                'text_align': 'left'
            }
        )
        
        PageWidget.objects.create(
            page=page,
            widget=intro_widget,
            order=2,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('✅ Added Introduction Text widget'))
        
        # 3. Product Section Widget (NEW!) - Featured Products
        featured_products_widget, _ = Widget.objects.get_or_create(
            name='Our Signature Products',
            defaults={
                'widget_type': 'product_section',
                'is_active': True
            }
        )
        
        # Get some products to feature
        products = Product.objects.filter(is_active=True)[:8]
        
        if products.exists():
            # Create WidgetProductSection content
            product_section, _ = WidgetProductSection.objects.get_or_create(
                widget=featured_products_widget,
                defaults={
                    'section_title': 'Our Signature Products'
                }
            )
            # Link products
            product_section.products.set(products)
            
            product_ids = list(products.values_list('id', flat=True))
            
            PageWidget.objects.create(
                page=page,
                widget=featured_products_widget,
                order=3,
                is_active=True,
                config={
                    'section_title': 'Our Signature Products',
                    'product_ids': product_ids
                }
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Added Product Section widget with {len(product_ids)} products'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  No products found to add to Product Section'))
        
        # 4. Text with Statistics Widget
        stats_widget, _ = Widget.objects.get_or_create(
            name='Our Achievements',
            defaults={
                'widget_type': 'text_with_stats',
                'is_active': True
            }
        )
        
        # Add statistics
        stats_data = [
            {'number': '50,000+', 'label': 'Happy Customers', 'order': 1},
            {'number': '500+', 'label': 'Trusted Vendors', 'order': 2},
            {'number': '10,000+', 'label': 'Products Available', 'order': 3},
            {'number': '99%', 'label': 'Customer Satisfaction', 'order': 4},
        ]
        
        for stat in stats_data:
            WidgetStatistic.objects.get_or_create(
                widget=stats_widget,
                order=stat['order'],
                defaults={
                    'number': stat['number'],
                    'label': stat['label']
                }
            )
        
        PageWidget.objects.create(
            page=page,
            widget=stats_widget,
            order=4,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('✅ Added Statistics widget'))
        
        # 5. Text Section Widget - Our Values
        values_widget, _ = Widget.objects.get_or_create(
            name='Our Values',
            defaults={
                'widget_type': 'text_section',
                'is_active': True
            }
        )
        
        WidgetTextSection.objects.get_or_create(
            widget=values_widget,
            defaults={
                'heading': 'What We Stand For',
                'content': '''<h3>Quality First</h3>
                <p>We never compromise on quality. Every product is carefully selected and tested.</p>
                
                <h3>Customer Satisfaction</h3>
                <p>Your happiness is our success. We go above and beyond to ensure you're satisfied.</p>
                
                <h3>Sustainability</h3>
                <p>We're committed to sustainable practices and eco-friendly products.</p>
                
                <h3>Community</h3>
                <p>We believe in building a community of conscious consumers and ethical vendors.</p>''',
                'text_align': 'left'
            }
        )
        
        PageWidget.objects.create(
            page=page,
            widget=values_widget,
            order=5,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('✅ Added Values Text widget'))
        
        # 6. Product Section Widget (NEW!) - Bestsellers
        bestsellers_widget, _ = Widget.objects.get_or_create(
            name='Customer Favorites',
            defaults={
                'widget_type': 'product_section',
                'is_active': True
            }
        )
        
        # Get different products for bestsellers
        bestseller_products = Product.objects.filter(is_active=True).order_by('-created_at')[:4]
        
        if bestseller_products.exists():
            # Create WidgetProductSection content
            bestseller_section, _ = WidgetProductSection.objects.get_or_create(
                widget=bestsellers_widget,
                defaults={
                    'section_title': 'Customer Favorites'
                }
            )
            # Link products
            bestseller_section.products.set(bestseller_products)
            
            bestseller_ids = list(bestseller_products.values_list('id', flat=True))
            
            PageWidget.objects.create(
                page=page,
                widget=bestsellers_widget,
                order=6,
                is_active=True,
                config={
                    'section_title': 'Customer Favorites',
                    'product_ids': bestseller_ids
                }
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Added Bestsellers Product Section with {len(bestseller_ids)} products'))
        
        # 7. FAQ Widget
        faq_widget, _ = Widget.objects.get_or_create(
            name='Story FAQs',
            defaults={
                'widget_type': 'faq_accordion',
                'is_active': True
            }
        )
        
        faqs_data = [
            {
                'question': 'How do you select your vendors?',
                'answer': '<p>We have a rigorous vetting process that includes quality checks, background verification, and customer feedback analysis. Only vendors who meet our high standards are approved.</p>',
                'order': 1
            },
            {
                'question': 'What makes your marketplace different?',
                'answer': '<p>We focus on quality over quantity. Every product is curated, every vendor is vetted, and every customer interaction is personalized. We\'re not just a marketplace; we\'re a community.</p>',
                'order': 2
            },
            {
                'question': 'Do you offer international shipping?',
                'answer': '<p>Yes! We ship to most countries worldwide. Shipping costs and delivery times vary by location. Check our shipping page for more details.</p>',
                'order': 3
            },
        ]
        
        for faq in faqs_data:
            WidgetFAQItem.objects.get_or_create(
                widget=faq_widget,
                order=faq['order'],
                defaults={
                    'question': faq['question'],
                    'answer': faq['answer']
                }
            )
        
        PageWidget.objects.create(
            page=page,
            widget=faq_widget,
            order=7,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('✅ Added FAQ widget'))
        
        # 8. HTML Content Widget - Call to Action
        cta_widget, _ = Widget.objects.get_or_create(
            name='Story CTA',
            defaults={
                'widget_type': 'html_content',
                'is_active': True
            }
        )
        
        WidgetHTMLContent.objects.get_or_create(
            widget=cta_widget,
            defaults={
                'html_content': '''
                <div style="background: linear-gradient(135deg, #064C50 0%, #0a6b70 100%); padding: 60px 20px; text-align: center; border-radius: 12px; margin: 40px 0;">
                    <h2 style="color: white; font-size: 36px; margin-bottom: 20px;">Ready to Start Shopping?</h2>
                    <p style="color: rgba(255,255,255,0.9); font-size: 18px; margin-bottom: 30px;">Join thousands of happy customers who trust us for their shopping needs.</p>
                    <a href="/shop" style="display: inline-block; background: white; color: #064C50; padding: 15px 40px; border-radius: 50px; text-decoration: none; font-weight: 600; font-size: 16px;">Browse Products</a>
                </div>
                ''',
                'css_classes': 'cta-section'
            }
        )
        
        PageWidget.objects.create(
            page=page,
            widget=cta_widget,
            order=8,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('✅ Added CTA HTML widget'))
        
        # Add page to navigation menu if not already there
        nav_menu, created = NavigationMenu.objects.get_or_create(
            title='Our Story',
            defaults={
                'url': f'/page/{page.slug}/',
                'order': 4,
                'is_active': True,
                'open_in_new_tab': False
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ Added "{nav_menu.title}" to navigation menu'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️  Navigation menu item already exists: {nav_menu.title}'))
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✅ Enhanced page builder seeding completed!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS(f'\n📄 Page URL: /page/{page.slug}/'))
        self.stdout.write(self.style.SUCCESS(f'🔗 Navigation: Added to main menu'))
        self.stdout.write(self.style.SUCCESS(f'🧩 Widgets: {page.page_widgets.count()} widgets added'))
        self.stdout.write(self.style.SUCCESS('\n📋 Widget Summary:'))
        self.stdout.write(self.style.SUCCESS('  1. 🎯 Dynamic Hero Banner (with button)'))
        self.stdout.write(self.style.SUCCESS('  2. 📝 Introduction Text'))
        self.stdout.write(self.style.SUCCESS(f'  3. 🛍️  Product Section - Signature Products ({len(product_ids)} products)'))
        self.stdout.write(self.style.SUCCESS('  4. 📊 Statistics (4 stats)'))
        self.stdout.write(self.style.SUCCESS('  5. 📝 Values Text'))
        self.stdout.write(self.style.SUCCESS(f'  6. 🛍️  Product Section - Customer Favorites ({len(bestseller_ids)} products)'))
        self.stdout.write(self.style.SUCCESS('  7. ❓ FAQ (3 questions)'))
        self.stdout.write(self.style.SUCCESS('  8. 💻 CTA HTML'))
        self.stdout.write(self.style.SUCCESS('\n👉 Visit the admin panel to see the page and widgets!'))
        self.stdout.write(self.style.SUCCESS('👉 Visit http://localhost:3000/page/our-story/ to see it live!'))
        self.stdout.write(self.style.SUCCESS('\n💡 Note: Dynamic Hero uses placeholder image. Upload actual image in admin for production.'))
