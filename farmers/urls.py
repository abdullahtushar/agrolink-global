"""
Farmers URL Configuration
"""

from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('crops/', views.my_crops, name='my_crops'),
    path('crops/add/', views.add_crop, name='add_crop'),
    path('crops/<int:pk>/edit/', views.edit_crop, name='edit_crop'),
    path('crops/<int:pk>/delete/', views.delete_crop, name='delete_crop'),
]
