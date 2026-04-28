"""
Dashboard URL Configuration
"""

from django.urls import path
from . import views

urlpatterns = [
    path('production/', views.production_map, name='production_map'),
    path('demand/', views.demand_intelligence, name='demand_intelligence'),
    path('profit-calculator/', views.profit_calculator, name='profit_calculator'),
    path('prediction/', views.prediction_view, name='prediction'),
]
