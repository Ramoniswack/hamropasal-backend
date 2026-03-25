"""
Quick test to verify Analytics Dashboard is accessible
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

print("="*60)
print("  Testing Analytics Dashboard Access")
print("="*60)

# Create a test client
client = Client()

# Get admin user
try:
    admin = User.objects.get(username='admin')
    print(f"\n✓ Admin user found: {admin.username}")
except User.DoesNotExist:
    print("\n✗ Admin user not found. Please create one first.")
    exit(1)

# Login as admin
client.force_login(admin)
print("✓ Logged in as admin")

# Test analytics dashboard URL
print("\nTesting Analytics Dashboard URL...")
response = client.get('/admin/analytics/')

if response.status_code == 200:
    print(f"✓ Analytics Dashboard is accessible!")
    print(f"✓ Status Code: {response.status_code}")
    print(f"✓ URL: http://localhost:8000/admin/analytics/")
    
    # Check if key content is in response
    content = response.content.decode('utf-8')
    if 'Analytics Dashboard' in content:
        print("✓ Page title found")
    if 'Total Revenue' in content:
        print("✓ Revenue section found")
    if 'Most Sold Products' in content:
        print("✓ Products section found")
    
    print("\n" + "="*60)
    print("  ✅ SUCCESS! Analytics Dashboard is working!")
    print("="*60)
    print("\nAccess it at:")
    print("  1. Top Menu: Click '📊 Analytics Dashboard'")
    print("  2. Direct URL: http://localhost:8000/admin/analytics/")
    print("  3. Sidebar: Under 'Authentication and Authorization'")
    
else:
    print(f"✗ Failed to access Analytics Dashboard")
    print(f"✗ Status Code: {response.status_code}")
    print(f"✗ Response: {response.content[:200]}")

print("\n" + "="*60)
