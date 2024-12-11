from django.urls import path
from . import views


app_name = 'station_details'

urlpatterns = [
    path('details/<int:station_id>/', views.station_details, name='station_details'),

    ]