"""
Farmers Views — Dashboard & Crop Management
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CropListing
from .forms import CropListingForm
from inquiries.models import Inquiry


def farmer_required(view_func):
    """Decorator to ensure only farmers access farmer views."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_farmer:
            messages.error(request, 'Access denied. Farmer account required.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@farmer_required
def farmer_dashboard(request):
    """Farmer's main dashboard."""
    listings = CropListing.objects.filter(farmer=request.user)
    inquiries = Inquiry.objects.filter(farmer=request.user).order_by('-created_at')[:5]
    total_listings = listings.count()
    available = listings.filter(status='available').count()
    total_inquiries = Inquiry.objects.filter(farmer=request.user).count()

    context = {
        'listings': listings[:6],
        'inquiries': inquiries,
        'total_listings': total_listings,
        'available': available,
        'total_inquiries': total_inquiries,
    }
    return render(request, 'farmers/dashboard.html', context)


@farmer_required
def add_crop(request):
    """Add a new crop listing."""
    if request.method == 'POST':
        form = CropListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.farmer = request.user
            listing.save()
            messages.success(request, 'Crop listing added successfully!')
            return redirect('farmer_dashboard')
    else:
        form = CropListingForm(initial={'district': request.user.district})

    return render(request, 'farmers/add_crop.html', {'form': form})


@farmer_required
def edit_crop(request, pk):
    """Edit an existing crop listing."""
    listing = get_object_or_404(CropListing, pk=pk, farmer=request.user)

    if request.method == 'POST':
        form = CropListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Crop listing updated successfully!')
            return redirect('farmer_dashboard')
    else:
        form = CropListingForm(instance=listing)

    return render(request, 'farmers/edit_crop.html', {'form': form, 'listing': listing})


@farmer_required
def delete_crop(request, pk):
    """Delete a crop listing."""
    listing = get_object_or_404(CropListing, pk=pk, farmer=request.user)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Crop listing deleted.')
        return redirect('farmer_dashboard')
    return render(request, 'farmers/delete_crop.html', {'listing': listing})


@farmer_required
def my_crops(request):
    """View all farmer's crops."""
    listings = CropListing.objects.filter(farmer=request.user)
    return render(request, 'farmers/my_crops.html', {'listings': listings})
