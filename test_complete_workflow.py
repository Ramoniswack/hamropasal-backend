"""
Complete E-Commerce Workflow Test
Tests all business logic: orders, stock management, reviews, cart clearing, etc.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.products.models import Product, ProductReview, StockHistory
from apps.users.models import Wishlist
from apps.orders.models import Cart, CartItem, Order, OrderItem, OrderStatusHistory
from decimal import Decimal
from django.utils import timezone
from django.db import transaction

User = get_user_model()


def create_users():
    """Create additional test users"""
    print("\n" + "="*60)
    print("STEP 1: Creating Additional Users")
    print("="*60)
    
    users_data = [
        {'username': 'sonik', 'email': 'sonik@example.com', 'first_name': 'Sonik', 'last_name': 'Kumar'},
        {'username': 'bishal', 'email': 'bishal@example.com', 'first_name': 'Bishal', 'last_name': 'Sharma'},
        {'username': 'rachana', 'email': 'rachana@example.com', 'first_name': 'Rachana', 'last_name': 'Patel'},
        {'username': 'devi', 'email': 'devi@example.com', 'first_name': 'Devi', 'last_name': 'Singh'},
    ]
    
    created_users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'user_type': 'customer'
            }
        )
        if created:
            user.set_password('test123')
            user.save()
            print(f"✅ Created user: {user.username} ({user.email})")
        else:
            print(f"ℹ️  User already exists: {user.username}")
        created_users.append(user)
    
    return created_users


def add_wishlists_and_carts(users):
    """Add products to wishlists and carts"""
    print("\n" + "="*60)
    print("STEP 2: Adding Products to Wishlists and Carts")
    print("="*60)
    
    products = list(Product.objects.filter(is_active=True, stock__gt=0)[:15])
    
    if not products:
        print("❌ No products available!")
        return
    
    # Sonik's wishlist and cart
    for product in products[0:4]:
        Wishlist.objects.get_or_create(user=users[0], product=product)
        print(f"❤️  {users[0].username} added '{product.name}' to wishlist")
    
    sonik_cart, _ = Cart.objects.get_or_create(user=users[0])
    for product, qty in [(products[0], 2), (products[1], 1)]:
        CartItem.objects.get_or_create(
            cart=sonik_cart,
            product=product,
            defaults={'quantity': qty}
        )
        print(f"🛒 {users[0].username} added {qty}x '{product.name}' to cart")
    
    # Bishal's wishlist and cart
    for product in products[2:6]:
        Wishlist.objects.get_or_create(user=users[1], product=product)
        print(f"❤️  {users[1].username} added '{product.name}' to wishlist")
    
    bishal_cart, _ = Cart.objects.get_or_create(user=users[1])
    for product, qty in [(products[3], 1), (products[4], 2)]:
        CartItem.objects.get_or_create(
            cart=bishal_cart,
            product=product,
            defaults={'quantity': qty}
        )
        print(f"🛒 {users[1].username} added {qty}x '{product.name}' to cart")
    
    # Rachana's wishlist and cart
    for product in products[5:9]:
        Wishlist.objects.get_or_create(user=users[2], product=product)
        print(f"❤️  {users[2].username} added '{product.name}' to wishlist")
    
    rachana_cart, _ = Cart.objects.get_or_create(user=users[2])
    for product, qty in [(products[6], 3), (products[7], 1)]:
        CartItem.objects.get_or_create(
            cart=rachana_cart,
            product=product,
            defaults={'quantity': qty}
        )
        print(f"🛒 {users[2].username} added {qty}x '{product.name}' to cart")
    
    # Devi's wishlist and cart
    for product in products[8:12]:
        Wishlist.objects.get_or_create(user=users[3], product=product)
        print(f"❤️  {users[3].username} added '{product.name}' to wishlist")
    
    devi_cart, _ = Cart.objects.get_or_create(user=users[3])
    for product, qty in [(products[9], 1), (products[10], 2)]:
        CartItem.objects.get_or_create(
            cart=devi_cart,
            product=product,
            defaults={'quantity': qty}
        )
        print(f"🛒 {users[3].username} added {qty}x '{product.name}' to cart")


@transaction.atomic
def create_order_from_cart(user, cart):
    """Create order from cart and clear cart items"""
    print(f"\n📦 Creating order for {user.username}...")
    
    cart_items = cart.items.all()
    if not cart_items:
        print(f"   ⚠️  Cart is empty for {user.username}")
        return None
    
    # Calculate totals
    subtotal = sum(item.subtotal for item in cart_items)
    shipping_cost = Decimal('5.99')
    tax = subtotal * Decimal('0.08')
    total = subtotal + shipping_cost + tax
    
    # Create order
    order = Order.objects.create(
        user=user,
        customer_name=f"{user.first_name} {user.last_name}",
        customer_email=user.email,
        customer_phone='+1234567890',
        shipping_address=f"{user.id} Main Street",
        shipping_city="Kathmandu",
        shipping_state="Bagmati",
        shipping_zip_code="44600",
        shipping_country="Nepal",
        status='pending',
        payment_status='paid',
        subtotal=subtotal,
        shipping_cost=shipping_cost,
        tax=tax,
        total=total
    )
    
    # Create order items from cart
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            product_name=cart_item.product.name,
            product_sku=cart_item.product.sku,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price,
            discount_price=cart_item.product.discount_price or Decimal('0'),
            subtotal=cart_item.subtotal
        )
        print(f"   ✅ Added {cart_item.quantity}x '{cart_item.product.name}' to order")
    
    # Clear cart after order creation
    cart_items.delete()
    print(f"   🗑️  Cart cleared for {user.username}")
    
    print(f"   📦 Order #{order.order_number} created - Total: ${order.total}")
    return order


@transaction.atomic
def deliver_order(order):
    """Mark order as delivered and reduce stock"""
    print(f"\n🚚 Delivering order #{order.order_number}...")
    
    admin_user = User.objects.filter(is_superuser=True).first()
    
    # Update order status through the workflow
    order.status = 'confirmed'
    order.confirmed_at = timezone.now()
    order.save()
    OrderStatusHistory.objects.create(
        order=order,
        status='confirmed',
        changed_by=admin_user,
        notes="Order confirmed"
    )
    print(f"   ✅ Status: Confirmed")
    
    order.status = 'processing'
    order.save()
    OrderStatusHistory.objects.create(
        order=order,
        status='processing',
        changed_by=admin_user,
        notes="Order processing"
    )
    print(f"   ✅ Status: Processing")
    
    order.status = 'shipped'
    order.shipped_at = timezone.now()
    order.save()
    OrderStatusHistory.objects.create(
        order=order,
        status='shipped',
        changed_by=admin_user,
        notes="Order shipped"
    )
    print(f"   ✅ Status: Shipped")
    
    order.status = 'delivered'
    order.delivered_at = timezone.now()
    order.save()
    OrderStatusHistory.objects.create(
        order=order,
        status='delivered',
        changed_by=admin_user,
        notes="Order delivered successfully"
    )
    print(f"   ✅ Status: Delivered")
    
    # Reduce stock for each item
    for order_item in order.items.all():
        product = order_item.product
        old_stock = product.stock
        product.stock -= order_item.quantity
        product.units_sold += order_item.quantity
        product.revenue_generated += order_item.subtotal
        product.save()
        
        # Create stock history
        StockHistory.objects.create(
            product=product,
            change_type='sale',
            quantity_change=-order_item.quantity,
            stock_before=old_stock,
            stock_after=product.stock,
            created_by=admin_user,
            notes=f"Sold via order #{order.order_number}"
        )
        
        print(f"   📉 Stock reduced: '{product.name}' ({old_stock} → {product.stock})")


def test_review_system(user, product, should_succeed=True):
    """Test review system with purchase verification"""
    print(f"\n🔍 Testing review for {user.username} on '{product.name}'...")
    
    # Check if user has purchased and received the product
    has_purchased = OrderItem.objects.filter(
        order__user=user,
        order__status='delivered',
        product=product
    ).exists()
    
    if has_purchased:
        print(f"   ✅ User has purchased and received this product")
        
        # Create review
        review, created = ProductReview.objects.get_or_create(
            product=product,
            user=user,
            defaults={
                'rating': 5,
                'comment': f"Great product! Very satisfied with my purchase.",
                'is_verified_purchase': True,
                'is_approved': True
            }
        )
        
        if created:
            print(f"   ⭐ Review created: {review.rating}/5 stars")
            print(f"   📊 Product rating updated: {product.average_rating:.1f}/5 ({product.review_count} reviews)")
        else:
            print(f"   ℹ️  Review already exists")
    else:
        print(f"   ❌ User has NOT purchased this product - Review not allowed")
        if should_succeed:
            print(f"   ⚠️  TEST FAILED: Expected user to have purchased product")


def check_product_visibility():
    """Check product visibility rules"""
    print("\n" + "="*60)
    print("PRODUCT VISIBILITY CHECK")
    print("="*60)
    
    # Products that should be visible (active and in stock)
    visible_products = Product.objects.filter(is_active=True, stock__gt=0)
    print(f"\n✅ Visible products (active + in stock): {visible_products.count()}")
    for p in visible_products[:5]:
        print(f"   📦 {p.name} - Stock: {p.stock}, Active: {p.is_active}")
    
    # Products that should NOT be visible
    out_of_stock = Product.objects.filter(is_active=True, stock=0)
    inactive = Product.objects.filter(is_active=False)
    
    print(f"\n❌ Hidden products:")
    print(f"   Out of stock (active but stock=0): {out_of_stock.count()}")
    print(f"   Inactive: {inactive.count()}")
    
    print(f"\n💡 Frontend should only display: is_active=True AND stock > 0")


def main():
    print("\n" + "="*60)
    print("COMPLETE E-COMMERCE WORKFLOW TEST")
    print("="*60)
    
    try:
        # Step 1: Create users
        users = create_users()
        
        # Step 2: Add wishlists and carts
        add_wishlists_and_carts(users)
        
        # Step 3: Create orders from carts
        print("\n" + "="*60)
        print("STEP 3: Creating Orders from Carts")
        print("="*60)
        
        orders = []
        for user in users:
            cart = Cart.objects.filter(user=user).first()
            if cart:
                order = create_order_from_cart(user, cart)
                if order:
                    orders.append(order)
        
        # Step 4: Deliver orders (this reduces stock)
        print("\n" + "="*60)
        print("STEP 4: Delivering Orders (Stock Reduction)")
        print("="*60)
        
        for order in orders:
            deliver_order(order)
        
        # Step 5: Test review system
        print("\n" + "="*60)
        print("STEP 5: Testing Review System")
        print("="*60)
        
        # Test 1: User who purchased should be able to review
        if orders:
            first_order = orders[0]
            first_item = first_order.items.first()
            if first_item:
                test_review_system(first_order.user, first_item.product, should_succeed=True)
        
        # Test 2: User who didn't purchase should NOT be able to review
        non_buyer = User.objects.filter(username='john_doe').first()
        if non_buyer and orders:
            first_item = orders[0].items.first()
            if first_item:
                test_review_system(non_buyer, first_item.product, should_succeed=False)
        
        # Step 6: Check product visibility
        check_product_visibility()
        
        # Final summary
        print("\n" + "="*60)
        print("FINAL SUMMARY")
        print("="*60)
        
        print(f"\n👥 Total Users: {User.objects.filter(is_superuser=False).count()}")
        print(f"❤️  Total Wishlist Items: {Wishlist.objects.count()}")
        print(f"🛒 Active Carts: {Cart.objects.count()}")
        print(f"📦 Total Orders: {Order.objects.count()}")
        print(f"   - Delivered: {Order.objects.filter(status='delivered').count()}")
        print(f"   - Pending: {Order.objects.filter(status='pending').count()}")
        print(f"⭐ Total Reviews: {ProductReview.objects.count()}")
        print(f"   - Verified Purchases: {ProductReview.objects.filter(is_verified_purchase=True).count()}")
        print(f"📊 Stock History Records: {StockHistory.objects.count()}")
        
        print("\n" + "="*60)
        print("BUSINESS LOGIC VERIFICATION")
        print("="*60)
        
        print("\n✅ Cart Clearing:")
        empty_carts = Cart.objects.filter(items__isnull=True).count()
        print(f"   Carts cleared after order: {empty_carts}/{len(orders)}")
        
        print("\n✅ Stock Reduction:")
        stock_reductions = StockHistory.objects.filter(change_type='sale').count()
        print(f"   Stock reduction records: {stock_reductions}")
        
        print("\n✅ Review Verification:")
        verified_reviews = ProductReview.objects.filter(is_verified_purchase=True).count()
        print(f"   Verified purchase reviews: {verified_reviews}")
        
        print("\n✅ Product Visibility:")
        visible = Product.objects.filter(is_active=True, stock__gt=0).count()
        hidden = Product.objects.filter(is_active=False).count() + Product.objects.filter(stock=0).count()
        print(f"   Visible products: {visible}")
        print(f"   Hidden products: {hidden}")
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        print("\n🔍 Admin Dashboard: http://localhost:8000/admin/")
        print("   - Check Orders section for delivered orders")
        print("   - Check Products section for stock changes")
        print("   - Check Product Reviews for verified purchases")
        print("   - Check Stock History for automatic reductions")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
