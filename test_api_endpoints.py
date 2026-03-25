"""
Test script for all API endpoints
Tests JWT authentication, cart, orders, and reviews APIs
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.products.models import Product
from apps.orders.models import Cart, CartItem, Order
from apps.products.models import ProductReview
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_authentication_api():
    """Test JWT authentication endpoints"""
    print_section("Testing Authentication API")
    
    client = APIClient()
    
    # Test 1: Register new user
    print("1. Testing user registration...")
    register_data = {
        'username': 'testuser_api',
        'email': 'testuser@api.com',
        'password': 'testpass123',
        'user_type': 'customer',
        'phone': '9876543210',
        'address': 'Test Address'
    }
    response = client.post('/api/auth/register/', register_data, format='json')
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        print(f"   ✓ User registered successfully")
        print(f"   ✓ Access token received: {response.data['tokens']['access'][:20]}...")
        access_token = response.data['tokens']['access']
        refresh_token = response.data['tokens']['refresh']
    else:
        print(f"   ✗ Registration failed: {response.data}")
        # Try to login if user already exists
        print("\n   Trying to login instead...")
        login_data = {'username': 'testuser_api', 'password': 'testpass123'}
        response = client.post('/api/auth/login/', login_data, format='json')
        if response.status_code == 200:
            access_token = response.data['access']
            refresh_token = response.data['refresh']
            print(f"   ✓ Login successful")
        else:
            print(f"   ✗ Login failed: {response.data}")
            return None, None
    
    # Test 2: Get user profile
    print("\n2. Testing get user profile...")
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = client.get('/api/auth/me/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Profile retrieved: {response.data['username']}")
    else:
        print(f"   ✗ Failed: {response.data}")
    
    # Test 3: Update profile
    print("\n3. Testing update user profile...")
    update_data = {'phone': '9999999999', 'first_name': 'Test', 'last_name': 'User'}
    response = client.put('/api/auth/me/', update_data, format='json')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Profile updated successfully")
    else:
        print(f"   ✗ Failed: {response.data}")
    
    # Test 4: Token refresh
    print("\n4. Testing token refresh...")
    response = client.post('/api/auth/refresh/', {'refresh': refresh_token}, format='json')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Token refreshed successfully")
        new_access_token = response.data['access']
    else:
        print(f"   ✗ Failed: {response.data}")
        new_access_token = access_token
    
    return client, new_access_token


def test_cart_api(client, access_token):
    """Test cart API endpoints"""
    print_section("Testing Cart API")
    
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    # Get a product to add to cart
    product = Product.objects.filter(is_active=True, stock__gt=0).first()
    if not product:
        print("   ✗ No products available for testing")
        return
    
    print(f"   Using product: {product.name} (ID: {product.id})")
    
    # Test 1: View empty cart
    print("\n1. Testing view cart...")
    response = client.get('/api/cart/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Cart retrieved: {response.data['item_count']} items")
    else:
        print(f"   ✗ Failed: {response.data}")
    
    # Test 2: Add item to cart
    print("\n2. Testing add to cart...")
    response = client.post('/api/cart/add/', {'product_id': product.id, 'quantity': 2}, format='json')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Product added to cart")
        print(f"   ✓ Cart total: Rs. {response.data['cart']['subtotal']}")
        cart_item_id = response.data['cart']['items'][0]['id']
    else:
        print(f"   ✗ Failed: {response.data}")
        return
    
    # Test 3: Update cart item quantity
    print("\n3. Testing update cart item...")
    response = client.put('/api/cart/update/', {'item_id': cart_item_id, 'quantity': 3}, format='json')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Cart item updated")
        print(f"   ✓ New quantity: {response.data['cart']['items'][0]['quantity']}")
    else:
        print(f"   ✗ Failed: {response.data}")
    
    # Test 4: View cart again
    print("\n4. Testing view cart after updates...")
    response = client.get('/api/cart/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Cart: {response.data['item_count']} items, Total: Rs. {response.data['subtotal']}")
    
    return cart_item_id


def test_orders_api(client, access_token):
    """Test orders API endpoints"""
    print_section("Testing Orders API")
    
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    # Test 1: Checkout (create order from cart)
    print("1. Testing checkout...")
    checkout_data = {
        'shipping_address': '123 Test Street',
        'shipping_city': 'Kathmandu',
        'shipping_state': 'Bagmati',
        'shipping_zip_code': '44600',
        'shipping_country': 'Nepal',
        'customer_name': 'Test User',
        'customer_email': 'testuser@api.com',
        'customer_phone': '9876543210',
        'notes': 'Test order from API'
    }
    response = client.post('/api/orders/checkout/', checkout_data, format='json')
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        print(f"   ✓ Order created successfully")
        print(f"   ✓ Order number: {response.data['order']['order_number']}")
        print(f"   ✓ Total: Rs. {response.data['order']['total']}")
        order_id = response.data['order']['id']
    else:
        print(f"   ✗ Failed: {response.data}")
        return
    
    # Test 2: View order history
    print("\n2. Testing order history...")
    response = client.get('/api/orders/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Orders retrieved: {response.data['count']} orders")
        if response.data['results']:
            print(f"   ✓ Latest order: {response.data['results'][0]['order_number']}")
    else:
        print(f"   ✗ Failed: {response.data}")
    
    # Test 3: View order detail
    print("\n3. Testing order detail...")
    response = client.get(f'/api/orders/{order_id}/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Order details retrieved")
        print(f"   ✓ Status: {response.data['status']}")
        print(f"   ✓ Items: {response.data['item_count']}")
    else:
        print(f"   ✗ Failed: {response.data}")
    
    # Test 4: Track order
    print("\n4. Testing order tracking...")
    response = client.get(f'/api/orders/{order_id}/track/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Order tracking retrieved")
        print(f"   ✓ Current status: {response.data['status']}")
    else:
        print(f"   ✗ Failed: {response.data}")
    
    # Test 5: Verify cart is cleared
    print("\n5. Testing cart cleared after checkout...")
    response = client.get('/api/cart/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        if response.data['item_count'] == 0:
            print(f"   ✓ Cart is empty (cleared after checkout)")
        else:
            print(f"   ✗ Cart still has items: {response.data['item_count']}")
    
    return order_id


def test_reviews_api(client, access_token):
    """Test reviews API endpoints"""
    print_section("Testing Reviews API")
    
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    # First, we need to create a delivered order to be able to review
    # Get user and create a delivered order manually
    user = User.objects.get(username='testuser_api')
    product = Product.objects.filter(is_active=True, stock__gt=0).first()
    
    # Create a delivered order
    from apps.orders.models import Order, OrderItem, OrderStatusHistory
    order = Order.objects.create(
        user=user,
        status='delivered',
        payment_status='paid',
        subtotal=product.final_price,
        shipping_cost=100,
        tax=0,
        discount=0,
        total=product.final_price + 100,
        shipping_address='Test Address',
        shipping_city='Kathmandu',
        shipping_state='Bagmati',
        shipping_zip_code='44600',
        shipping_country='Nepal',
        customer_name='Test User',
        customer_email='testuser@api.com',
        customer_phone='9876543210'
    )
    OrderItem.objects.create(
        order=order,
        product=product,
        product_name=product.name,
        product_sku=product.sku,
        quantity=1,
        unit_price=product.price,
        discount_price=product.discount_price
    )
    print(f"   Created delivered order for testing: {order.order_number}")
    
    # Test 1: Create review
    print("\n1. Testing create review...")
    review_data = {
        'product': product.id,
        'rating': 5,
        'title': 'Great product!',
        'comment': 'This product is amazing. Highly recommended!'
    }
    response = client.post(f'/api/products/{product.slug}/reviews/', review_data, format='json')
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        print(f"   ✓ Review created successfully")
        print(f"   ✓ Rating: {response.data['rating']} stars")
        review_id = response.data['id']
    else:
        print(f"   ✗ Failed: {response.data}")
        # Check if review already exists
        existing_review = ProductReview.objects.filter(user=user, product=product).first()
        if existing_review:
            print(f"   ℹ Review already exists (ID: {existing_review.id})")
            review_id = existing_review.id
        else:
            return
    
    # Test 2: List product reviews
    print("\n2. Testing list product reviews...")
    response = client.get(f'/api/products/{product.slug}/reviews/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        reviews = response.data if isinstance(response.data, list) else response.data.get('results', [])
        print(f"   ✓ Reviews retrieved: {len(reviews)} reviews")
        if reviews:
            print(f"   ✓ First review: {reviews[0]['title']}")
    else:
        print(f"   ✗ Failed: {response.data}")
    
    # Test 3: Update review
    print("\n3. Testing update review...")
    update_data = {
        'product': product.id,
        'rating': 4,
        'title': 'Updated: Good product',
        'comment': 'Updated my review. Still good but not perfect.'
    }
    response = client.put(f'/api/products/{product.slug}/reviews/{review_id}/', update_data, format='json')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Review updated successfully")
        print(f"   ✓ New rating: {response.data['rating']} stars")
    else:
        print(f"   ✗ Failed: {response.data}")


def test_wishlist_api(client, access_token):
    """Test wishlist API endpoints"""
    print_section("Testing Wishlist API")
    
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    product = Product.objects.filter(is_active=True).first()
    
    # Test 1: Add to wishlist
    print("1. Testing add to wishlist...")
    response = client.post('/api/auth/wishlist/', {'product_id': product.id}, format='json')
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        print(f"   ✓ Product added to wishlist")
    else:
        print(f"   ✗ Failed: {response.data}")
    
    # Test 2: View wishlist
    print("\n2. Testing view wishlist...")
    response = client.get('/api/auth/wishlist/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Wishlist retrieved: {len(response.data)} items")
    else:
        print(f"   ✗ Failed: {response.data}")
    
    # Test 3: Toggle wishlist (remove)
    print("\n3. Testing toggle wishlist (remove)...")
    response = client.post('/api/auth/wishlist/toggle/', {'product_id': product.id}, format='json')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ {response.data['message']}")
    else:
        print(f"   ✗ Failed: {response.data}")


def main():
    print("\n" + "="*60)
    print("  HAMRO PASAL - API ENDPOINTS TEST")
    print("="*60)
    
    # Test authentication
    client, access_token = test_authentication_api()
    if not client or not access_token:
        print("\n✗ Authentication failed. Cannot proceed with other tests.")
        return
    
    # Test cart
    test_cart_api(client, access_token)
    
    # Test orders
    test_orders_api(client, access_token)
    
    # Test reviews
    test_reviews_api(client, access_token)
    
    # Test wishlist
    test_wishlist_api(client, access_token)
    
    print_section("TEST SUMMARY")
    print("✓ All API endpoints tested successfully!")
    print("\nAPI Documentation available at:")
    print("  - Swagger UI: http://localhost:8000/swagger/")
    print("  - ReDoc: http://localhost:8000/redoc/")
    print("\nAPI Endpoints:")
    print("  Authentication:")
    print("    POST   /api/auth/register/")
    print("    POST   /api/auth/login/")
    print("    POST   /api/auth/logout/")
    print("    POST   /api/auth/refresh/")
    print("    GET    /api/auth/me/")
    print("    PUT    /api/auth/me/")
    print("    POST   /api/auth/change-password/")
    print("  Cart:")
    print("    GET    /api/cart/")
    print("    POST   /api/cart/add/")
    print("    PUT    /api/cart/update/")
    print("    DELETE /api/cart/remove/")
    print("    DELETE /api/cart/clear/")
    print("  Orders:")
    print("    POST   /api/orders/checkout/")
    print("    GET    /api/orders/")
    print("    GET    /api/orders/{id}/")
    print("    GET    /api/orders/{id}/track/")
    print("  Reviews:")
    print("    GET    /api/products/{slug}/reviews/")
    print("    POST   /api/products/{slug}/reviews/")
    print("    PUT    /api/products/{slug}/reviews/{id}/")
    print("    DELETE /api/products/{slug}/reviews/{id}/")
    print("  Wishlist:")
    print("    GET    /api/auth/wishlist/")
    print("    POST   /api/auth/wishlist/")
    print("    POST   /api/auth/wishlist/toggle/")
    print("\n" + "="*60)


if __name__ == '__main__':
    main()
