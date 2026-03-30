# Quick Start Guide

Get the Hamro Pasal backend running in 5 minutes!

## Prerequisites

- Python 3.10+
- PostgreSQL installed
- Git

## Setup Steps

### 1. Clone & Install

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Create Database

```bash
# Create PostgreSQL database
createdb hamropasal
```

### 3. Configure Environment

Create `.env` file in backend directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=hamropasal
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 4. Setup Database

```bash
# Run migrations
python manage.py migrate

# Load sample data (recommended)
python manage.py loaddata hamropasal_data.json

# OR create superuser manually
python manage.py createsuperuser
```

### 5. Run Server

```bash
python manage.py runserver
```

## Access Points

- **Admin Panel**: http://localhost:8000/admin/
- **API Docs (Swagger)**: http://localhost:8000/swagger/
- **API Docs (ReDoc)**: http://localhost:8000/redoc/
- **Analytics Dashboard**: http://localhost:8000/admin/analyticsDashboard/

## What's Included in the Dump?

The `hamropasal_data.json` file includes:
- ✅ Sample products with categories
- ✅ CMS pages and widgets
- ✅ Blog posts
- ✅ Navigation menus
- ✅ Site settings
- ✅ Banners
- ✅ Sample users (you may need to reset passwords)

## Common Issues

### "relation does not exist"
Run migrations first: `python manage.py migrate`

### "password authentication failed"
Check your `.env` file has correct PostgreSQL credentials

### "No such file: hamropasal_data.json"
Make sure you're in the `backend` directory

## Next Steps

1. ✅ Read [README.md](README.md) for complete documentation
2. ✅ Read [DATABASE_SETUP.md](DATABASE_SETUP.md) for detailed database guide
3. ✅ Read [PAGE_BUILDER_GUIDE.md](../PAGE_BUILDER_GUIDE.md) for Page Builder tutorial
4. ✅ Explore the API at http://localhost:8000/swagger/
5. ✅ Check the Analytics Dashboard at http://localhost:8000/admin/analyticsDashboard/

## Need Help?

- Check [DATABASE_SETUP.md](DATABASE_SETUP.md) for troubleshooting
- Check [README.md](README.md) for complete API documentation
- Contact the team lead

---

**Happy Coding! 🚀**
