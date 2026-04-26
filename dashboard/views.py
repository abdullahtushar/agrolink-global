"""
Dashboard Views — Home, Production Map, Demand Intelligence, Profit Calculator
"""

from django.shortcuts import render
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from farmers.models import CropListing, Vegetable
from accounts.models import User


def home_view(request):
    """Landing page."""
    stats = {
        'total_farmers': User.objects.filter(role='farmer').count(),
        'total_exporters': User.objects.filter(role='exporter').count(),
        'total_crops': CropListing.objects.filter(status='available').count(),
        'total_vegetables': Vegetable.objects.count(),
    }
    from .utils import get_profitable_predictions
    predictions = get_profitable_predictions()

    # Featured listings
    featured = CropListing.objects.filter(status='available').select_related('vegetable', 'farmer')[:6]
    return render(request, 'dashboard/home.html', {
        'stats': stats, 
        'featured': featured,
        'predictions': predictions
    })


@login_required
def production_map(request):
    """District-based production data view."""
    # Aggregate production by district
    district_data = (
        CropListing.objects
        .filter(status='available')
        .values('district')
        .annotate(
            total_quantity=Sum('quantity_kg'),
            total_listings=Count('id'),
            crop_types=Count('vegetable', distinct=True),
        )
        .order_by('-total_quantity')
    )

    # Aggregate by crop type
    crop_data = (
        CropListing.objects
        .filter(status='available')
        .values('vegetable__name')
        .annotate(
            total_quantity=Sum('quantity_kg'),
            total_listings=Count('id'),
            district_count=Count('district', distinct=True),
        )
        .order_by('-total_quantity')
    )

    context = {
        'district_data': district_data,
        'crop_data': crop_data,
    }
    return render(request, 'dashboard/production_map.html', context)


@login_required
def demand_intelligence(request):
    """Static mock data for EU/US demand trends."""
    # Mock demand data — simulating real market intelligence
    eu_trends = [
        {'vegetable': 'Potato', 'demand_level': 'High', 'avg_price_usd': 0.45, 'trend': 'up', 'change': '+12%', 'notes': 'Strong demand across Western Europe'},
        {'vegetable': 'Onion', 'demand_level': 'High', 'avg_price_usd': 0.52, 'trend': 'up', 'change': '+8%', 'notes': 'Supply shortage in Spain driving prices'},
        {'vegetable': 'Tomato', 'demand_level': 'Medium', 'avg_price_usd': 1.20, 'trend': 'stable', 'change': '+2%', 'notes': 'Stable demand, seasonal variations'},
        {'vegetable': 'Green Chili', 'demand_level': 'Medium', 'avg_price_usd': 2.10, 'trend': 'up', 'change': '+15%', 'notes': 'Growing ethnic food market'},
        {'vegetable': 'Bitter Gourd', 'demand_level': 'Low', 'avg_price_usd': 1.80, 'trend': 'up', 'change': '+20%', 'notes': 'Niche Asian grocery segment'},
        {'vegetable': 'Eggplant', 'demand_level': 'Medium', 'avg_price_usd': 0.95, 'trend': 'stable', 'change': '+3%', 'notes': 'Mediterranean cuisine driving demand'},
        {'vegetable': 'Cauliflower', 'demand_level': 'High', 'avg_price_usd': 0.75, 'trend': 'up', 'change': '+10%', 'notes': 'Health food trend boosting demand'},
        {'vegetable': 'Cabbage', 'demand_level': 'Medium', 'avg_price_usd': 0.35, 'trend': 'down', 'change': '-5%', 'notes': 'Oversupply from local EU farms'},
    ]

    us_trends = [
        {'vegetable': 'Potato', 'demand_level': 'High', 'avg_price_usd': 0.55, 'trend': 'stable', 'change': '+3%', 'notes': 'Steady fast-food industry demand'},
        {'vegetable': 'Onion', 'demand_level': 'High', 'avg_price_usd': 0.60, 'trend': 'up', 'change': '+6%', 'notes': 'Restaurant recovery post-pandemic'},
        {'vegetable': 'Tomato', 'demand_level': 'High', 'avg_price_usd': 1.45, 'trend': 'up', 'change': '+9%', 'notes': 'Year-round demand, organic premium'},
        {'vegetable': 'Green Chili', 'demand_level': 'High', 'avg_price_usd': 2.50, 'trend': 'up', 'change': '+18%', 'notes': 'Mexican & Asian food popularity'},
        {'vegetable': 'Bitter Gourd', 'demand_level': 'Medium', 'avg_price_usd': 2.20, 'trend': 'up', 'change': '+25%', 'notes': 'Health-conscious consumer growth'},
        {'vegetable': 'Eggplant', 'demand_level': 'Medium', 'avg_price_usd': 1.10, 'trend': 'up', 'change': '+7%', 'notes': 'Plant-based diet popularity'},
        {'vegetable': 'Cauliflower', 'demand_level': 'High', 'avg_price_usd': 0.90, 'trend': 'up', 'change': '+14%', 'notes': 'Cauliflower-based products booming'},
        {'vegetable': 'Cabbage', 'demand_level': 'Medium', 'avg_price_usd': 0.40, 'trend': 'stable', 'change': '+1%', 'notes': 'Coleslaw & Asian food markets'},
    ]

    me_trends = [
        {'vegetable': 'Potato', 'demand_level': 'High', 'avg_price_usd': 0.65, 'trend': 'up', 'change': '+15%', 'notes': 'High consumption in Gulf states'},
        {'vegetable': 'Onion', 'demand_level': 'High', 'avg_price_usd': 0.70, 'trend': 'stable', 'change': '+5%', 'notes': 'Essential for local cuisine'},
        {'vegetable': 'Tomato', 'demand_level': 'High', 'avg_price_usd': 1.10, 'trend': 'up', 'change': '+12%', 'notes': 'Constant demand year-round'},
        {'vegetable': 'Green Chili', 'demand_level': 'Medium', 'avg_price_usd': 2.00, 'trend': 'up', 'change': '+20%', 'notes': 'High demand from South Asian expat communities'},
        {'vegetable': 'Bitter Gourd', 'demand_level': 'Medium', 'avg_price_usd': 2.50, 'trend': 'up', 'change': '+18%', 'notes': 'Popular among Asian expats'},
        {'vegetable': 'Eggplant', 'demand_level': 'Medium', 'avg_price_usd': 0.85, 'trend': 'stable', 'change': '+2%', 'notes': 'Used in traditional Middle Eastern dishes'},
        {'vegetable': 'Cauliflower', 'demand_level': 'Medium', 'avg_price_usd': 1.00, 'trend': 'up', 'change': '+8%', 'notes': 'Growing popularity in modern cuisine'},
        {'vegetable': 'Cabbage', 'demand_level': 'Low', 'avg_price_usd': 0.45, 'trend': 'stable', 'change': '+0%', 'notes': 'Steady, moderate demand'},
    ]

    context = {
        'eu_trends': eu_trends,
        'us_trends': us_trends,
        'me_trends': me_trends,
    }
    return render(request, 'dashboard/demand_intelligence.html', context)


def profit_calculator(request):
    """Profit estimation tool."""
    result = None
    if request.method == 'POST':
        try:
            production_cost = float(request.POST.get('production_cost', 0))
            transport_cost = float(request.POST.get('transport_cost', 0))
            selling_price = float(request.POST.get('selling_price', 0))
            quantity = float(request.POST.get('quantity', 0))

            total_cost = (production_cost + transport_cost) * quantity
            total_revenue = selling_price * quantity
            profit = total_revenue - total_cost
            profit_margin = (profit / total_revenue * 100) if total_revenue > 0 else 0

            result = {
                'production_cost': production_cost,
                'transport_cost': transport_cost,
                'selling_price': selling_price,
                'quantity': quantity,
                'total_cost': round(total_cost, 2),
                'total_revenue': round(total_revenue, 2),
                'profit': round(profit, 2),
                'profit_margin': round(profit_margin, 2),
                'is_profitable': profit > 0,
            }
        except (ValueError, ZeroDivisionError):
            result = {'error': 'Please enter valid numbers.'}

    return render(request, 'dashboard/profit_calculator.html', {'result': result})

def farmers_list(request):
    """List of all registered farmers."""
    farmers = User.objects.filter(role='farmer').order_by('-date_joined')
    return render(request, 'dashboard/farmers_list.html', {'farmers': farmers})

def exporters_list(request):
    """List of all active exporters."""
    exporters = User.objects.filter(role='exporter').order_by('-date_joined')
    return render(request, 'dashboard/exporters_list.html', {'exporters': exporters})

def crops_list(request):
    """List of all available crops with images."""
    vegetables = Vegetable.objects.all().order_by('name')
    return render(request, 'dashboard/crops_list.html', {'vegetables': vegetables})

def predictions_list(request):
    """Predicted profitable crops."""
    from .utils import get_profitable_predictions
    predictions = get_profitable_predictions()
    return render(request, 'dashboard/predictions_list.html', {'predictions': predictions})
