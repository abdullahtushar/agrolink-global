def get_profitable_predictions():
    """
    Returns the top 3 profitable crops for the next 30 days based on region multipliers.
    Formula: profit = selling_price - (production_cost + transport_cost)
    Multipliers: EU = 1.2, US = 1.3, Middle East = 1.1
    """
    
    # Mock base data for calculation (prices in BDT for 1 KG)
    crops_data = [
        {'name': 'Green Chili', 'base_selling_price': 250, 'production_cost': 60, 'transport_cost': 40},
        {'name': 'Tomato', 'base_selling_price': 140, 'production_cost': 30, 'transport_cost': 30},
        {'name': 'Bitter Gourd', 'base_selling_price': 220, 'production_cost': 50, 'transport_cost': 40},
        {'name': 'Eggplant', 'base_selling_price': 100, 'production_cost': 20, 'transport_cost': 25},
        {'name': 'Cauliflower', 'base_selling_price': 90, 'production_cost': 25, 'transport_cost': 25},
    ]

    regions = [
        {'name': 'US', 'multiplier': 1.3},
        {'name': 'EU', 'multiplier': 1.2},
        {'name': 'Middle East', 'multiplier': 1.1},
    ]

    from farmers.models import Vegetable
    
    predictions = []

    for crop in crops_data:
        try:
            veg = Vegetable.objects.get(name=crop['name'])
            image_url = veg.image.url if veg.image else None
        except Vegetable.DoesNotExist:
            image_url = None
            
        for region in regions:
            # Apply regional multiplier to the selling price
            adjusted_selling_price = crop['base_selling_price'] * region['multiplier']
            
            # Calculate profit
            profit = adjusted_selling_price - (crop['production_cost'] + crop['transport_cost'])
            
            predictions.append({
                'name': crop['name'],
                'region': region['name'],
                'profit': round(profit, 2),
                'image_url': image_url
            })

    # Sort by profit descending and get top 3
    predictions.sort(key=lambda x: x['profit'], reverse=True)
    return predictions[:3]

def get_top_profitable_crops():
    from farmers.models import CropListing
    from django.utils import timezone
    import datetime

    # Simple season mapping
    current_month = timezone.now().month
    if 3 <= current_month <= 6:
        current_season = 'kharif1'
    elif 7 <= current_month <= 10:
        current_season = 'kharif2'
    else:
        current_season = 'rabi'

    listings = CropListing.objects.filter(status='available').select_related('vegetable')
    
    results = []
    estimated_cost = 30
    
    for listing in listings:
        veg = listing.vegetable
        demand_score = veg.demand_score
        price_per_kg = float(listing.price_per_kg)
        
        is_in_season = (veg.season == current_season) or (veg.season == 'year_round')
        season_factor = 1.2 if is_in_season else 0.8
        
        profit_score = (demand_score * price_per_kg * season_factor) - estimated_cost
        
        results.append({
            'listing': listing,
            'vegetable': veg,
            'profit_score': round(profit_score, 2),
            'season_factor': season_factor,
            'is_in_season': is_in_season
        })
        
    results.sort(key=lambda x: x['profit_score'], reverse=True)
    return results[:5]
