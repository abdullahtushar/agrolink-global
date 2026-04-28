"""
Farmers Models — Crop & Production Data
"""

import os
from django.db import models
from django.conf import settings
from django.templatetags.static import static


class Vegetable(models.Model):
    """Vegetable/Crop catalog."""

    class Season(models.TextChoices):
        KHARIF1 = 'kharif1', 'Kharif-1 (Mar–Jun)'
        KHARIF2 = 'kharif2', 'Kharif-2 (Jul–Oct)'
        RABI = 'rabi', 'Rabi (Nov–Feb)'
        YEAR_ROUND = 'year_round', 'Year Round'

    name = models.CharField(max_length=100)
    local_name = models.CharField(max_length=100, blank=True, help_text='Name in Bangla/local language')
    description = models.TextField(blank=True)
    season = models.CharField(max_length=20, choices=Season.choices, default=Season.RABI)
    image = models.ImageField(upload_to='vegetables/', blank=True, null=True)
    demand_score = models.FloatField(default=0.5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vegetables'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def static_image_url(self):
        """Return static URL for the vegetable image (works on Render)."""
        if self.image:
            # Map media filename to static path
            filename = os.path.basename(self.image.name)
            return static(f'images/vegetables/{filename}')
        return None


class CropListing(models.Model):
    """Farmer's crop production listing."""

    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        SOLD = 'sold', 'Sold Out'
        UPCOMING = 'upcoming', 'Upcoming'

    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='crop_listings',
        limit_choices_to={'role': 'farmer'},
    )
    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE, related_name='listings')
    quantity_kg = models.DecimalField(max_digits=10, decimal_places=2, help_text='Quantity in KG')
    price_per_kg = models.DecimalField(max_digits=8, decimal_places=2, help_text='Price per KG in BDT')
    district = models.CharField(max_length=100)
    season = models.CharField(max_length=20, choices=Vegetable.Season.choices)
    harvest_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.AVAILABLE)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'crop_listings'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.vegetable.name} — {self.quantity_kg}kg by {self.farmer.get_full_name()}"

    @property
    def total_value(self):
        return self.quantity_kg * self.price_per_kg
