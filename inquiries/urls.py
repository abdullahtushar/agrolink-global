"""
Inquiries URL Configuration
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.inquiry_list, name='inquiry_list'),
    path('<int:pk>/', views.inquiry_detail, name='inquiry_detail'),
]
