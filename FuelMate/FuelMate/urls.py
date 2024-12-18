# FuelMate/urls.py (or your project-level urls.py)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_panel/', include('admin_panel.urls')),
    path('', include('stations.urls')),
    path('accounts/', include('accounts.urls')),
    path('maps/', include('maps.urls')),
    path('profil_account/', include('profil_account.urls')),
    path('locate_station/', include('locate_station.urls')),
    path('add_prices/', include('add_prices.urls')),
    path('price_history/', include('price_history.urls')),
    path('ranking/', include('ranking.urls')),
    path('station_details/', include('station_details.urls')),


]

