"""
Accounts Models — Custom User with Role-Based Access
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended user model with role support."""

    class Role(models.TextChoices):
        FARMER = 'farmer', 'Farmer'
        EXPORTER = 'exporter', 'Exporter'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.FARMER,
    )
    phone = models.CharField(max_length=20, blank=True)
    district = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    @property
    def is_farmer(self):
        return self.role == self.Role.FARMER

    @property
    def is_exporter(self):
        return self.role == self.Role.EXPORTER

    @property
    def is_admin_user(self):
        return self.role == self.Role.ADMIN
