from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'user_type', 'first_name', 'last_name', 'is_staff', 'is_active', 'created_at']
    list_filter = ['user_type', 'is_staff', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    
    def get_readonly_fields(self, request, obj=None):
        """Make customer information read-only for existing users"""
        if obj:  # Editing an existing user
            if obj.user_type == 'customer':
                # For customers, make all personal info read-only
                return [
                    'username', 'email', 'first_name', 'last_name', 'phone', 'address',
                    'user_type', 'last_login', 'date_joined', 'created_at', 'updated_at'
                ]
            else:
                # For staff/vendors, only timestamps are read-only
                return ['last_login', 'date_joined', 'created_at', 'updated_at']
        return ['created_at', 'updated_at']
    
    def get_fieldsets(self, request, obj=None):
        """Customize fieldsets based on user type - hide password for customers"""
        if obj and obj.user_type == 'customer':
            # For customers: view-only mode, NO password field
            return (
                ('Customer Account (Read-Only)', {
                    'fields': ('username',),
                    'description': 'Customer information is read-only. Customers manage their own data and passwords.'
                }),
                ('Personal Information (Read-Only)', {
                    'fields': ('first_name', 'last_name', 'email', 'phone', 'address'),
                }),
                ('Account Type', {
                    'fields': ('user_type',)
                }),
                ('Account Status', {
                    'fields': ('is_active',),
                    'description': 'You can activate/deactivate customer accounts.'
                }),
                ('Important Dates', {
                    'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
                    'classes': ('collapse',)
                }),
            )
        else:
            # For staff/vendors: full access
            return (
                (None, {'fields': ('username', 'password')}),
                ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'address')}),
                ('User Type', {'fields': ('user_type',)}),
                ('Permissions', {
                    'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
                }),
                ('Important dates', {
                    'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
                    'classes': ('collapse',)
                }),
            )
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of customer accounts"""
        if obj and obj.user_type == 'customer':
            return False
        return super().has_delete_permission(request, obj)
    
    def changelist_view(self, request, extra_context=None):
        """Add custom message to user list view"""
        extra_context = extra_context or {}
        extra_context['title'] = 'Users (Customer data is read-only)'
        return super().changelist_view(request, extra_context=extra_context)
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )


# NOTE: Wishlist is intentionally NOT registered in admin
# Wishlist is private user data and should not be accessible to admin
# Admin can see aggregate statistics (wishlist count) in the Product admin
