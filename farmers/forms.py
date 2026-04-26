"""
Farmers Forms — Crop Listing Management
"""

from django import forms
from .models import CropListing, Vegetable
from accounts.forms import DISTRICTS


class CropListingForm(forms.ModelForm):
    """Form for creating/editing crop listings."""

    district = forms.ChoiceField(
        choices=DISTRICTS,
        widget=forms.Select(attrs={'class': 'form-input'}),
    )

    class Meta:
        model = CropListing
        fields = ['vegetable', 'quantity_kg', 'price_per_kg', 'district', 'season', 'harvest_date', 'status', 'description']
        widgets = {
            'vegetable': forms.Select(attrs={'class': 'form-input'}),
            'quantity_kg': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Quantity in KG', 'step': '0.01'}),
            'price_per_kg': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Price per KG (BDT)', 'step': '0.01'}),
            'season': forms.Select(attrs={'class': 'form-input'}),
            'harvest_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Additional details about your crop...'}),
        }
