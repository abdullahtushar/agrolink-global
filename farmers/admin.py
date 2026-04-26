"""
Farmers Admin Configuration
"""

from django.contrib import admin
from .models import Vegetable, CropListing


@admin.register(Vegetable)
class VegetableAdmin(admin.ModelAdmin):
    list_display = ('name', 'local_name', 'season', 'created_at')
    list_filter = ('season',)
    search_fields = ('name', 'local_name')


@admin.register(CropListing)
class CropListingAdmin(admin.ModelAdmin):
    list_display = ('vegetable', 'farmer', 'quantity_kg', 'price_per_kg', 'district', 'status', 'created_at')
    list_filter = ('status', 'season', 'district')
    search_fields = ('vegetable__name', 'farmer__username', 'district')
    raw_id_fields = ('farmer',)
