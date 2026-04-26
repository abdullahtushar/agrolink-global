"""
Exporters Views — Search, Dashboard & Inquiry Sending
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from farmers.models import CropListing, Vegetable
from inquiries.models import Inquiry
from inquiries.forms import InquiryForm
from accounts.forms import DISTRICTS


def exporter_required(view_func):
    """Decorator to ensure only exporters access exporter views."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_exporter:
            messages.error(request, 'Access denied. Exporter account required.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@exporter_required
def exporter_dashboard(request):
    """Exporter's main dashboard with search and stats."""
    listings = CropListing.objects.filter(status='available')
    total_available = listings.count()
    total_inquiries = Inquiry.objects.filter(exporter=request.user).count()
    pending_inquiries = Inquiry.objects.filter(exporter=request.user, status='pending').count()

    # Get search parameters
    search_query = request.GET.get('q', '')
    district_filter = request.GET.get('district', '')
    crop_filter = request.GET.get('crop', '')
    season_filter = request.GET.get('season', '')

    if search_query:
        listings = listings.filter(
            Q(vegetable__name__icontains=search_query) |
            Q(district__icontains=search_query) |
            Q(farmer__first_name__icontains=search_query)
        )
    if district_filter:
        listings = listings.filter(district=district_filter)
    if crop_filter:
        listings = listings.filter(vegetable_id=crop_filter)
    if season_filter:
        listings = listings.filter(season=season_filter)

    vegetables = Vegetable.objects.all()
    districts = [d for d in DISTRICTS if d[0]]  # Remove empty choice

    from dashboard.utils import get_profitable_predictions
    predictions = get_profitable_predictions()

    context = {
        'listings': listings,
        'total_available': total_available,
        'total_inquiries': total_inquiries,
        'pending_inquiries': pending_inquiries,
        'vegetables': vegetables,
        'districts': districts,
        'seasons': Vegetable.Season.choices,
        'search_query': search_query,
        'district_filter': district_filter,
        'crop_filter': crop_filter,
        'season_filter': season_filter,
        'predictions': predictions,
    }
    return render(request, 'exporters/dashboard.html', context)


@exporter_required
def listing_detail(request, pk):
    """View a specific crop listing."""
    listing = get_object_or_404(CropListing, pk=pk)
    return render(request, 'exporters/listing_detail.html', {'listing': listing})


@exporter_required
def send_inquiry(request, listing_pk):
    """Send an inquiry to a farmer about a listing."""
    listing = get_object_or_404(CropListing, pk=listing_pk)

    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.exporter = request.user
            inquiry.farmer = listing.farmer
            inquiry.crop_listing = listing
            inquiry.save()
            messages.success(request, 'Inquiry sent successfully!')
            return redirect('exporter_dashboard')
    else:
        form = InquiryForm(initial={
            'subject': f'Inquiry about {listing.vegetable.name} — {listing.quantity_kg}kg',
        })

    return render(request, 'exporters/send_inquiry.html', {'form': form, 'listing': listing})


@exporter_required
def my_inquiries(request):
    """View all exporter's inquiries."""
    inquiries = Inquiry.objects.filter(exporter=request.user)
    return render(request, 'exporters/my_inquiries.html', {'inquiries': inquiries})
