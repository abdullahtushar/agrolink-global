"""
Inquiries Admin Configuration
"""

from django.contrib import admin
from .models import Inquiry, InquiryReply


class InquiryReplyInline(admin.TabularInline):
    model = InquiryReply
    extra = 0
    readonly_fields = ('sender', 'message', 'created_at')


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('subject', 'exporter', 'farmer', 'crop_listing', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('subject', 'exporter__username', 'farmer__username')
    raw_id_fields = ('exporter', 'farmer', 'crop_listing')
    inlines = [InquiryReplyInline]


@admin.register(InquiryReply)
class InquiryReplyAdmin(admin.ModelAdmin):
    list_display = ('inquiry', 'sender', 'created_at')
    raw_id_fields = ('inquiry', 'sender')
