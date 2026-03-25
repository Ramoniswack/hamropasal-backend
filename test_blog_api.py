"""
Test Blog API Endpoints
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.test import Client
from apps.blog.models import BlogPost, BlogCategory, BlogTag

print("="*70)
print("  Testing Blog API Endpoints")
print("="*70)

client = Client()

# Test Blog Posts List
print("\n[1] Testing Blog Posts List API...")
response = client.get('/api/blog/posts/')
if response.status_code == 200:
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Total Posts: {data.get('count', 0)}")
    if data.get('results'):
        print(f"✓ First Post: {data['results'][0]['title']}")
else:
    print(f"✗ Failed: {response.status_code}")

# Test Blog Post Detail
print("\n[2] Testing Blog Post Detail API...")
first_post = BlogPost.objects.filter(is_published=True).first()
if first_post:
    response = client.get(f'/api/blog/posts/{first_post.slug}/')
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Post Title: {data['title']}")
        print(f"✓ Category: {data['category']['name']}")
        print(f"✓ Tags: {len(data['tags'])}")
        print(f"✓ Comments: {len(data['comments'])}")
    else:
        print(f"✗ Failed: {response.status_code}")
else:
    print("✗ No published posts found")

# Test Blog Categories
print("\n[3] Testing Blog Categories API...")
response = client.get('/api/blog/categories/')
if response.status_code == 200:
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    if isinstance(data, list):
        print(f"✓ Total Categories: {len(data)}")
        if data:
            print(f"✓ First Category: {data[0]['name']}")
    else:
        print(f"✓ Total Categories: {data.get('count', 0)}")
else:
    print(f"✗ Failed: {response.status_code}")

# Test Blog Tags
print("\n[4] Testing Blog Tags API...")
response = client.get('/api/blog/tags/')
if response.status_code == 200:
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    if isinstance(data, list):
        print(f"✓ Total Tags: {len(data)}")
    else:
        print(f"✓ Total Tags: {data.get('count', 0)}")
else:
    print(f"✗ Failed: {response.status_code}")

# Test Featured Posts
print("\n[5] Testing Featured Posts API...")
response = client.get('/api/blog/posts/featured/')
if response.status_code == 200:
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Featured Posts: {len(data)}")
else:
    print(f"✗ Failed: {response.status_code}")

# Test Popular Posts
print("\n[6] Testing Popular Posts API...")
response = client.get('/api/blog/posts/popular/')
if response.status_code == 200:
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Popular Posts: {len(data)}")
else:
    print(f"✗ Failed: {response.status_code}")

# Test Recent Posts
print("\n[7] Testing Recent Posts API...")
response = client.get('/api/blog/posts/recent/')
if response.status_code == 200:
    data = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Recent Posts: {len(data)}")
else:
    print(f"✗ Failed: {response.status_code}")

print("\n" + "="*70)
print("  ✅ Blog API Testing Complete!")
print("="*70)
print("\nBlog API Endpoints:")
print("  - GET  /api/blog/posts/                    - List all posts")
print("  - GET  /api/blog/posts/{slug}/             - Get post detail")
print("  - GET  /api/blog/posts/featured/           - Get featured posts")
print("  - GET  /api/blog/posts/popular/            - Get popular posts")
print("  - GET  /api/blog/posts/recent/             - Get recent posts")
print("  - GET  /api/blog/posts/{slug}/related/     - Get related posts")
print("  - GET  /api/blog/categories/               - List categories")
print("  - GET  /api/blog/categories/{slug}/        - Get category detail")
print("  - GET  /api/blog/tags/                     - List tags")
print("  - GET  /api/blog/tags/{slug}/              - Get tag detail")
print("  - GET  /api/blog/comments/?post={id}       - Get comments for post")
print("  - POST /api/blog/comments/                 - Create comment")
print("\n" + "="*70)
