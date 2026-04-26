"""
Accounts Admin Configuration
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'district', 'is_active')
    list_filter = ('role', 'is_active', 'district')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('AgroLink Profile', {
            'fields': ('role', 'phone', 'district', 'address', 'profile_picture'),
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('AgroLink Profile', {
            'fields': ('role', 'phone', 'district'),
        }),
    )
