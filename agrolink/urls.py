"""
AgroLink Global — Main URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import home_view
import dashboard.views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    
    # New Top-Level Stats Routes
    path('farmers/', dashboard_views.farmers_list, name='farmers_list'),
    path('exporters/', dashboard_views.exporters_list, name='exporters_list'),
    path('crops/', dashboard_views.crops_list, name='crops_list'),
    path('predictions/', dashboard_views.predictions_list, name='predictions_list'),
    
    path('accounts/', include('accounts.urls')),
    path('farmers/', include('farmers.urls')), # Note: exact match 'farmers/' handled above
    path('exporters/', include('exporters.urls')),
    path('inquiries/', include('inquiries.urls')),
    path('dashboard/', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
