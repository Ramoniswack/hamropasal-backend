"""
Test Analytics Dashboard via Proxy Model
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import site

User = get_user_model()

print("="*70)
print("  Testing Analytics Dashboard via Proxy Model")
print("="*70)

# Check if AnalyticsProxy is registered
from apps.core.admin import AnalyticsProxy
print(f"\n✓ AnalyticsProxy model imported successfully")

# Check if it's registered in admin
if AnalyticsProxy in site._registry:
    print(f"✓ AnalyticsProxy is registered in admin site")
    admin_class = site._registry[AnalyticsProxy]
    print(f"✓ Admin class: {admin_class.__class__.__name__}")
else:
    print(f"✗ AnalyticsProxy is NOT registered in admin site")

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

# Test the proxy model changelist URL
print("\nTesting Analytics Dashboard via Proxy Model...")
response = client.get('/admin/core/analyticsproxy/')

if response.status_code == 200:
    print(f"✓ Analytics Dashboard is accessible via proxy model!")
    print(f"✓ Status Code: {response.status_code}")
    print(f"✓ URL: http://localhost:8000/admin/core/analyticsproxy/")
    
    # Check if key content is in response
    content = response.content.decode('utf-8')
    if 'Analytics Dashboard' in content:
        print("✓ Page title found")
    if 'Total Revenue' in content:
        print("✓ Revenue section found")
    if 'Most Sold Products' in content:
        print("✓ Products section found")
    
    print("\n" + "="*70)
    print("  ✅ SUCCESS! Analytics Dashboard is working!")
    print("="*70)
    print("\nAccess it at:")
    print("  1. Admin Sidebar: Look for 'Core' section → '📊 Analytics Dashboard'")
    print("  2. Direct URL: http://localhost:8000/admin/core/analyticsproxy/")
    print("\nThe Analytics Dashboard will appear in the sidebar under the 'Core' app!")
    
else:
    print(f"✗ Failed to access Analytics Dashboard")
    print(f"✗ Status Code: {response.status_code}")
    if response.status_code == 404:
        print(f"✗ URL not found - the proxy model might not be registered correctly")
    print(f"✗ Response: {response.content[:200]}")

print("\n" + "="*70)
