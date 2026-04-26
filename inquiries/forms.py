"""
Inquiries Forms
"""

from django import forms
from .models import Inquiry, InquiryReply


class InquiryForm(forms.ModelForm):
    """Form for creating an inquiry."""

    class Meta:
        model = Inquiry
        fields = ['subject', 'message', 'quantity_needed']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Subject of inquiry'}),
            'message': forms.Textarea(attrs={'class': 'form-input', 'rows': 5, 'placeholder': 'Describe your requirements...'}),
            'quantity_needed': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Quantity needed (KG)', 'step': '0.01'}),
        }


class InquiryReplyForm(forms.ModelForm):
    """Form for replying to an inquiry."""

    class Meta:
        model = InquiryReply
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Type your reply...'}),
        }


class InquiryStatusForm(forms.ModelForm):
    """Form for updating inquiry status (farmer only)."""

    class Meta:
        model = Inquiry
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-input'}),
        }
