from django.urls import path
from . import views

urlpatterns = [
    path('map/', views.tomtom_map, name='tomtom_map'),
    path('api/gas_stations/', views.gas_stations_list, name='gas_stations_list'),

]
