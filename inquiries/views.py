"""
Inquiries Views — Communication System
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Inquiry, InquiryReply
from .forms import InquiryReplyForm, InquiryStatusForm


@login_required
def inquiry_list(request):
    """List inquiries for the current user."""
    if request.user.is_exporter:
        inquiries = Inquiry.objects.filter(exporter=request.user)
    elif request.user.is_farmer:
        inquiries = Inquiry.objects.filter(farmer=request.user)
    else:
        inquiries = Inquiry.objects.all()

    return render(request, 'inquiries/inquiry_list.html', {'inquiries': inquiries})


@login_required
def inquiry_detail(request, pk):
    """View inquiry thread with replies."""
    inquiry = get_object_or_404(Inquiry, pk=pk)

    # Ensure user is either the farmer or exporter in this inquiry
    if not (request.user == inquiry.exporter or request.user == inquiry.farmer or request.user.is_admin_user):
        messages.error(request, 'Access denied.')
        return redirect('inquiry_list')

    replies = inquiry.replies.all()
    reply_form = InquiryReplyForm()
    status_form = InquiryStatusForm(instance=inquiry) if request.user == inquiry.farmer else None

    if request.method == 'POST':
        if 'reply' in request.POST:
            reply_form = InquiryReplyForm(request.POST)
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.inquiry = inquiry
                reply.sender = request.user
                reply.save()
                # Auto-update status when farmer replies
                if request.user == inquiry.farmer and inquiry.status == 'pending':
                    inquiry.status = 'responded'
                    inquiry.save()
                messages.success(request, 'Reply sent!')
                return redirect('inquiry_detail', pk=pk)

        elif 'update_status' in request.POST and request.user == inquiry.farmer:
            status_form = InquiryStatusForm(request.POST, instance=inquiry)
            if status_form.is_valid():
                status_form.save()
                messages.success(request, 'Inquiry status updated!')
                return redirect('inquiry_detail', pk=pk)

    context = {
        'inquiry': inquiry,
        'replies': replies,
        'reply_form': reply_form,
        'status_form': status_form,
    }
    return render(request, 'inquiries/inquiry_detail.html', context)
