# Database Setup Guide

## Using the Database Dump

This repository includes a database dump file (`hamropasal_data.json`) with sample data to help you get started quickly.

### Prerequisites

- Python 3.10+
- PostgreSQL installed and running
- Virtual environment activated
- All dependencies installed (`pip install -r requirements.txt`)

---

## Option 1: Load from Dump File (Recommended)

### Step 1: Create Database

```bash
# Create PostgreSQL database
createdb hamropasal

# Or using psql
psql -U postgres
CREATE DATABASE hamropasal;
\q
```

### Step 2: Configure Environment

Update your `.env` file with database credentials:

```env
DB_NAME=hamropasal
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### Step 3: Run Migrations

```bash
cd backend
python manage.py migrate
```

### Step 4: Load Data from Dump

```bash
python manage.py loaddata hamropasal_data.json
```

This will load:
- Sample products with images
- Categories
- CMS pages and widgets
- Blog posts
- Banners
- Site settings
- Navigation menus
- Users (see credentials below)

### Step 5: Create Your Superuser (Optional)

If you want to create your own admin account:

```bash
python manage.py createsuperuser
```

Or use the existing admin account from the dump (see below).

---

## Option 2: Fresh Database Setup

If you prefer to start with an empty database:

### Step 1: Create Database

```bash
createdb hamropasal
```

### Step 2: Run Migrations

```bash
cd backend
python manage.py migrate
```

### Step 3: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 4: (Optional) Seed Sample Data

```bash
python manage.py seed_homepage_content
```

---

## Default Credentials (From Dump)

If you loaded data from `hamropasal_data.json`, you can use these credentials:

### Admin Account
- **Email**: Check the dump or create new superuser
- **Password**: You'll need to reset password or create new superuser

### Test Users
- Various test users may be included in the dump
- Use "Forgot Password" feature or create new accounts

**Security Note**: For production, always create new admin accounts and never use default credentials!

---

## Verifying the Setup

### 1. Start the Server

```bash
python manage.py runserver
```

### 2. Check Admin Panel

Visit: `http://localhost:8000/admin/`

You should see:
- Products in the database
- Categories configured
- CMS pages created
- Blog posts available

### 3. Check API

Visit: `http://localhost:8000/swagger/`

Test endpoints:
- `GET /api/products/` - Should return products
- `GET /api/categories/` - Should return categories
- `GET /api/cms/pages/` - Should return pages

### 4. Check Analytics Dashboard

Visit: `http://localhost:8000/admin/analyticsDashboard/`

Should display:
- Revenue metrics
- Order statistics
- Product data
- Charts and graphs

---

## Troubleshooting

### Error: "relation does not exist"

**Solution**: Run migrations first
```bash
python manage.py migrate
```

### Error: "duplicate key value violates unique constraint"

**Solution**: Database already has data. Either:
1. Drop and recreate database:
```bash
dropdb hamropasal
createdb hamropasal
python manage.py migrate
python manage.py loaddata hamropasal_data.json
```

2. Or use `--ignorenonexistent` flag:
```bash
python manage.py loaddata --ignorenonexistent hamropasal_data.json
```

### Error: "No such file or directory: hamropasal_data.json"

**Solution**: Make sure you're in the backend directory
```bash
cd backend
python manage.py loaddata hamropasal_data.json
```

### Error: "FATAL: password authentication failed"

**Solution**: Check your `.env` file has correct database credentials

### Media Files Missing

The dump only includes database data, not uploaded media files. You'll need to:
1. Upload new images through admin panel, or
2. Copy the `media/` folder from another team member

---

## Creating a New Dump

If you want to create a fresh dump with your current data:

```bash
# Full dump (recommended)
python manage.py dumpdata --indent 2 \
  --exclude core.analyticsproxy \
  --exclude contenttypes \
  --exclude auth.permission \
  --exclude sessions.session \
  --exclude admin.logentry \
  -o hamropasal_data.json

# Specific apps only
python manage.py dumpdata products categories cms blog banners \
  --indent 2 -o hamropasal_data.json
```

---

## Database Schema

The database includes these main tables:

### Products
- `products_product` - Product catalog
- `products_productimage` - Product images
- `products_productreview` - Customer reviews
- `products_producttag` - Product tags
- `products_stockhistory` - Inventory tracking

### Categories
- `categories_category` - Product categories (hierarchical)

### Orders
- `orders_order` - Customer orders
- `orders_orderitem` - Order line items
- `orders_cart` - Shopping carts
- `orders_cartitem` - Cart items

### Users
- `users_user` - Custom user model
- `users_wishlist` - User wishlists

### CMS
- `cms_page` - Custom pages
- `cms_widget` - Widget definitions
- `cms_pagewidget` - Page-widget relationships
- `cms_widgetdynamichero` - Hero banner content
- `cms_widgettextsection` - Text section content
- `cms_widgetproductsection` - Product section content
- `cms_navigationmenu` - Navigation menus
- `cms_footercolumn` - Footer columns
- `cms_footerlink` - Footer links
- `cms_sitesettings` - Site configuration

### Blog
- `blog_blogpost` - Blog posts
- `blog_blogcategory` - Blog categories
- `blog_blogtag` - Blog tags
- `blog_blogcomment` - Blog comments

### Banners
- `banners_herobanner` - Hero banners
- `banners_marketplacebanner` - Marketplace banners
- `banners_promobanner` - Promotional banners
- `banners_scrollingbanner` - Scrolling text banners

---

## Best Practices

### For Development
1. Use the dump file to get started quickly
2. Create your own superuser account
3. Don't commit sensitive data to git
4. Use `.env` for database credentials

### For Production
1. Never use dump data in production
2. Create fresh database with migrations
3. Use strong passwords
4. Enable database backups
5. Use environment variables for all secrets

### For Team Collaboration
1. Update the dump file when schema changes
2. Document any manual data setup steps
3. Keep media files in separate storage
4. Use database migrations for schema changes

---

## Additional Resources

- **Django Migrations**: https://docs.djangoproject.com/en/4.2/topics/migrations/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Django Fixtures**: https://docs.djangoproject.com/en/4.2/howto/initial-data/

---

## Support

If you encounter issues:
1. Check this guide's troubleshooting section
2. Verify all prerequisites are met
3. Check Django logs for error details
4. Contact the team lead

---

**Last Updated**: March 28, 2026
