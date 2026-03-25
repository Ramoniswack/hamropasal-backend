"""
Test E-Commerce Workflow
Creates test users, carts, wishlists, and orders to verify the complete system
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.products.models import Product
from apps.users.models import Wishlist
from apps.orders.models import Cart, CartItem, Order, OrderItem, OrderStatusHistory
from decimal import Decimal
from django.utils import timezone

User = get_user_model()

def create_test_users():
    """Create test users"""
    print("\n" + "="*60)
    print("STEP 1: Creating Test Users")
    print("="*60)
    
    users_data = [
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'test123',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '+1234567890',
            'user_type': 'customer'
        },
        {
            'username': 'jane_smith',
            'email': 'jane@example.com',
            'password': 'test123',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'phone': '+1234567891',
            'user_type': 'customer'
        },
        {
            'username': 'bob_wilson',
            'email': 'bob@example.com',
            'password': 'test123',
            'first_name': 'Bob',
            'last_name': 'Wilson',
            'phone': '+1234567892',
            'user_type': 'customer'
        }
    ]
    
    created_users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'phone': user_data['phone'],
                'user_type': user_data['user_type']
            }
        )
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"✅ Created user: {user.username} ({user.email})")
        else:
            print(f"ℹ️  User already exists: {user.username}")
        created_users.append(user)
    
    return created_users


def add_to_wishlists(users):
    """Add products to user wishlists"""
    print("\n" + "="*60)
    print("STEP 2: Adding Products to Wishlists")
    print("="*60)
    
    products = list(Product.objects.filter(is_active=True)[:10])
    
    if not products:
        print("❌ No products found! Run seed_all_data first.")
        return
    
    # John adds 3 products to wishlist
    john_wishlist = [products[0], products[2], products[4]]
    for product in john_wishlist:
        wishlist, created = Wishlist.objects.get_or_create(
            user=users[0],
            product=product
        )
        if created:
            print(f"❤️  {users[0].username} added '{product.name}' to wishlist")
    
    # Jane adds 2 products to wishlist
    jane_wishlist = [products[1], products[3]]
    for product in jane_wishlist:
        wishlist, created = Wishlist.objects.get_or_create(
            user=users[1],
            product=product
        )
        if created:
            print(f"❤️  {users[1].username} added '{product.name}' to wishlist")
    
    # Bob adds 4 products to wishlist
    bob_wishlist = [products[0], products[1], products[5], products[6]]
    for product in bob_wishlist:
        wishlist, created = Wishlist.objects.get_or_create(
            user=users[2],
            product=product
        )
        if created:
            print(f"❤️  {users[2].username} added '{product.name}' to wishlist")
    
    print(f"\n📊 Total wishlists created: {Wishlist.objects.count()}")


def add_to_carts(users):
    """Add products to user carts"""
    print("\n" + "="*60)
    print("STEP 3: Adding Products to Carts")
    print("="*60)
    
    products = list(Product.objects.filter(is_active=True)[:10])
    
    # John's cart
    john_cart, _ = Cart.objects.get_or_create(user=users[0])
    john_items = [
        (products[0], 2),
        (products[1], 1),
        (products[3], 3)
    ]
    for product, quantity in john_items:
        cart_item, created = CartItem.objects.get_or_create(
            cart=john_cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if created:
            print(f"🛒 {users[0].username} added {quantity}x '{product.name}' to cart")
    
    # Jane's cart
    jane_cart, _ = Cart.objects.get_or_create(user=users[1])
    jane_items = [
        (products[2], 1),
        (products[4], 2)
    ]
    for product, quantity in jane_items:
        cart_item, created = CartItem.objects.get_or_create(
            cart=jane_cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if created:
            print(f"🛒 {users[1].username} added {quantity}x '{product.name}' to cart")
    
    # Bob's cart
    bob_cart, _ = Cart.objects.get_or_create(user=users[2])
    bob_items = [
        (products[5], 1),
        (products[6], 2),
        (products[7], 1)
    ]
    for product, quantity in bob_items:
        cart_item, created = CartItem.objects.get_or_create(
            cart=bob_cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if created:
            print(f"🛒 {users[2].username} added {quantity}x '{product.name}' to cart")
    
    print(f"\n📊 Total carts: {Cart.objects.count()}")
    print(f"📊 Total cart items: {CartItem.objects.count()}")


def create_orders(users):
    """Create orders (simulate checkout)"""
    print("\n" + "="*60)
    print("STEP 4: Creating Orders (Simulating Checkout)")
    print("="*60)
    
    products = list(Product.objects.filter(is_active=True)[:10])
    admin_user = User.objects.filter(is_superuser=True).first()
    
    # Order 1: John's order (will be CONFIRMED by admin)
    order1 = Order.objects.create(
        user=users[0],
        customer_name=f"{users[0].first_name} {users[0].last_name}",
        customer_email=users[0].email,
        customer_phone=users[0].phone,
        shipping_address="123 Main St, Apt 4B",
        shipping_city="New York",
        shipping_state="NY",
        shipping_zip_code="10001",
        shipping_country="USA",
        status='pending',
        payment_status='paid',
        subtotal=Decimal('0'),
        shipping_cost=Decimal('5.99'),
        tax=Decimal('0'),
        discount=Decimal('0'),
        total=Decimal('0')
    )
    
    # Add items to order 1
    order1_items = [
        (products[0], 2, products[0].final_price),
        (products[1], 1, products[1].final_price),
    ]
    order1_subtotal = Decimal('0')
    for product, quantity, price in order1_items:
        subtotal = price * quantity
        order1_subtotal += subtotal
        OrderItem.objects.create(
            order=order1,
            product=product,
            product_name=product.name,
            product_sku=product.sku,
            quantity=quantity,
            unit_price=price,
            discount_price=product.discount_price or Decimal('0'),
            subtotal=subtotal
        )
    
    order1.subtotal = order1_subtotal
    order1.tax = order1_subtotal * Decimal('0.08')  # 8% tax
    order1.total = order1.subtotal + order1.shipping_cost + order1.tax
    order1.save()
    
    print(f"📦 Order #{order1.order_number} created for {users[0].username}")
    print(f"   Status: {order1.status} | Total: ${order1.total}")
    
    # Order 2: Jane's order (will be CANCELLED by admin)
    order2 = Order.objects.create(
        user=users[1],
        customer_name=f"{users[1].first_name} {users[1].last_name}",
        customer_email=users[1].email,
        customer_phone=users[1].phone,
        shipping_address="456 Oak Avenue",
        shipping_city="Los Angeles",
        shipping_state="CA",
        shipping_zip_code="90001",
        shipping_country="USA",
        status='pending',
        payment_status='paid',
        subtotal=Decimal('0'),
        shipping_cost=Decimal('5.99'),
        tax=Decimal('0'),
        discount=Decimal('0'),
        total=Decimal('0')
    )
    
    # Add items to order 2
    order2_items = [
        (products[2], 1, products[2].final_price),
        (products[4], 3, products[4].final_price),
    ]
    order2_subtotal = Decimal('0')
    for product, quantity, price in order2_items:
        subtotal = price * quantity
        order2_subtotal += subtotal
        OrderItem.objects.create(
            order=order2,
            product=product,
            product_name=product.name,
            product_sku=product.sku,
            quantity=quantity,
            unit_price=price,
            discount_price=product.discount_price or Decimal('0'),
            subtotal=subtotal
        )
    
    order2.subtotal = order2_subtotal
    order2.tax = order2_subtotal * Decimal('0.08')
    order2.total = order2.subtotal + order2.shipping_cost + order2.tax
    order2.save()
    
    print(f"📦 Order #{order2.order_number} created for {users[1].username}")
    print(f"   Status: {order2.status} | Total: ${order2.total}")
    
    # Order 3: Bob's order (will stay PENDING)
    order3 = Order.objects.create(
        user=users[2],
        customer_name=f"{users[2].first_name} {users[2].last_name}",
        customer_email=users[2].email,
        customer_phone=users[2].phone,
        shipping_address="789 Pine Road",
        shipping_city="Chicago",
        shipping_state="IL",
        shipping_zip_code="60601",
        shipping_country="USA",
        status='pending',
        payment_status='pending',
        subtotal=Decimal('0'),
        shipping_cost=Decimal('5.99'),
        tax=Decimal('0'),
        discount=Decimal('0'),
        total=Decimal('0')
    )
    
    # Add items to order 3
    order3_items = [
        (products[5], 2, products[5].final_price),
        (products[6], 1, products[6].final_price),
    ]
    order3_subtotal = Decimal('0')
    for product, quantity, price in order3_items:
        subtotal = price * quantity
        order3_subtotal += subtotal
        OrderItem.objects.create(
            order=order3,
            product=product,
            product_name=product.name,
            product_sku=product.sku,
            quantity=quantity,
            unit_price=price,
            discount_price=product.discount_price or Decimal('0'),
            subtotal=subtotal
        )
    
    order3.subtotal = order3_subtotal
    order3.tax = order3_subtotal * Decimal('0.08')
    order3.total = order3.subtotal + order3.shipping_cost + order3.tax
    order3.save()
    
    print(f"📦 Order #{order3.order_number} created for {users[2].username}")
    print(f"   Status: {order3.status} | Total: ${order3.total}")
    
    print(f"\n📊 Total orders created: {Order.objects.count()}")
    
    return [order1, order2, order3]


def simulate_admin_actions(orders):
    """Simulate admin managing orders"""
    print("\n" + "="*60)
    print("STEP 5: Simulating Admin Actions")
    print("="*60)
    
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("⚠️  No admin user found. Creating one...")
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
    
    # Confirm order 1
    order1 = orders[0]
    order1.status = 'confirmed'
    order1.confirmed_at = timezone.now()
    order1.save()
    OrderStatusHistory.objects.create(
        order=order1,
        status='confirmed',
        changed_by=admin_user,
        notes="Order confirmed by admin - ready for processing"
    )
    print(f"✅ Order #{order1.order_number} CONFIRMED by admin")
    
    # Cancel order 2
    order2 = orders[1]
    order2.status = 'cancelled'
    order2.save()
    OrderStatusHistory.objects.create(
        order=order2,
        status='cancelled',
        changed_by=admin_user,
        notes="Order cancelled - customer requested cancellation"
    )
    print(f"❌ Order #{order2.order_number} CANCELLED by admin")
    
    # Order 3 stays pending
    print(f"⏳ Order #{orders[2].order_number} remains PENDING (no action taken)")


def print_summary():
    """Print summary of all data"""
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    
    print(f"\n👥 Users: {User.objects.filter(is_superuser=False).count()} customers")
    print(f"❤️  Wishlists: {Wishlist.objects.count()} items")
    print(f"🛒 Active Carts: {Cart.objects.count()}")
    print(f"📦 Orders: {Order.objects.count()}")
    print(f"   - Pending: {Order.objects.filter(status='pending').count()}")
    print(f"   - Confirmed: {Order.objects.filter(status='confirmed').count()}")
    print(f"   - Cancelled: {Order.objects.filter(status='cancelled').count()}")
    
    print("\n" + "="*60)
    print("ADMIN DASHBOARD CHECK")
    print("="*60)
    print("\n✅ Go to: http://localhost:8000/admin/")
    print("   Login: admin / admin123")
    print("\n📋 What to verify:")
    print("   1. Orders section shows 3 orders")
    print("   2. Order statuses: 1 confirmed, 1 cancelled, 1 pending")
    print("   3. Cart/Wishlist sections are NOT visible (privacy)")
    print("   4. Products show 'In Carts' and 'In Wishlists' counts")
    print("   5. Order items show correct products and quantities")
    print("   6. Order status history shows admin actions")
    
    print("\n" + "="*60)
    print("PRIVACY CHECK")
    print("="*60)
    print("\n✅ Verify in Product Admin:")
    
    # Show some products with cart/wishlist counts
    products = Product.objects.filter(is_active=True)[:5]
    for product in products:
        cart_count = CartItem.objects.filter(product=product).count()
        wishlist_count = Wishlist.objects.filter(product=product).count()
        if cart_count > 0 or wishlist_count > 0:
            print(f"   📦 {product.name}")
            print(f"      🛒 In {cart_count} cart(s)")
            print(f"      ❤️  In {wishlist_count} wishlist(s)")
            print(f"      ⚠️  Admin should NOT see which users!")


def main():
    print("\n" + "="*60)
    print("E-COMMERCE WORKFLOW TEST")
    print("="*60)
    print("This script will:")
    print("1. Create test users")
    print("2. Add products to wishlists")
    print("3. Add products to carts")
    print("4. Create orders (simulate checkout)")
    print("5. Simulate admin actions (confirm/cancel orders)")
    print("="*60)
    
    try:
        users = create_test_users()
        add_to_wishlists(users)
        add_to_carts(users)
        orders = create_orders(users)
        simulate_admin_actions(orders)
        print_summary()
        
        print("\n✅ Workflow test completed successfully!")
        print("🔍 Now check the admin dashboard to verify everything works.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
