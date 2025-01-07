from django.urls import path
from . import views


app_name = 'station_details'

urlpatterns = [
    path('details/<int:station_id>/', views.station_details, name='station_details'),
    path('details/<int:station_id>/id_station_rating/', views.add_station_rating, name='add_station_rating'),

    path('details/<int:station_id>/add', views.station_add, name='station_add'),
    path('details/<int:station_id>/remove', views.station_remove, name='station_remove'),
    ]