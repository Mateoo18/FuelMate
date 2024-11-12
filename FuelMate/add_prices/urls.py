
from django.urls import path
from . import views
urlpatterns = [
    path('add_prices/', views.nearest_stations, name='nearest_stations'),
    path('add_prices/<int:station_id>/', views.station_details, name='station_details'),
]