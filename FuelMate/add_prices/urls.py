
from django.urls import path
from . import views
app_name = 'add_prices'
urlpatterns = [
    path('add_prices/', views.nearest_stations, name='nearest_stations'),
    path('add_prices/<int:Station_Id>/list', views.station_to_list, name='station_to_list'),
    path('add_prices/<int:Station_Id>/update', views.update_prices, name='update_prices'),
    path('add_prices/<int:Station_Id>/report_complain/', views.report_complain, name='report_complain'),
]