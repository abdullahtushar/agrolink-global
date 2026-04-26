"""
Exporters URL Configuration
"""

from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.exporter_dashboard, name='exporter_dashboard'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listing/<int:listing_pk>/inquiry/', views.send_inquiry, name='send_inquiry'),
    path('inquiries/', views.my_inquiries, name='my_inquiries'),
]
