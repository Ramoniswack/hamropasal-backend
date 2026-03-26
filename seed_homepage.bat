@echo off
echo 🌱 Seeding Homepage Content...
echo.

python manage.py seed_homepage_content

echo.
echo ✅ Done! Check your homepage at http://localhost:3000/
echo 📊 Check Django admin at http://localhost:8000/admin/
pause
