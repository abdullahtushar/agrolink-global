"""
Inquiries Models — Exporter-Farmer Communication
"""

from django.db import models
from django.conf import settings


class Inquiry(models.Model):
    """Inquiry from Exporter to Farmer."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        RESPONDED = 'responded', 'Responded'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
        CLOSED = 'closed', 'Closed'

    exporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_inquiries',
        limit_choices_to={'role': 'exporter'},
    )
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_inquiries',
        limit_choices_to={'role': 'farmer'},
    )
    crop_listing = models.ForeignKey(
        'farmers.CropListing',
        on_delete=models.CASCADE,
        related_name='inquiries',
    )
    subject = models.CharField(max_length=200)
    message = models.TextField()
    quantity_needed = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='Quantity needed in KG')
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inquiries'
        ordering = ['-created_at']
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        return f"Inquiry: {self.subject} ({self.get_status_display()})"


class InquiryReply(models.Model):
    """Reply messages on an inquiry thread."""

    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name='replies')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inquiry_replies'
        ordering = ['created_at']
        verbose_name_plural = 'Inquiry Replies'

    def __str__(self):
        return f"Reply by {self.sender.get_full_name()} on {self.inquiry.subject}"
