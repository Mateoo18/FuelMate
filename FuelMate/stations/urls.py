
from django.urls import path,include
from . import views

urlpatterns = [
    path('fuel/', views.fuel_list, name='fuel_list'),
    path('', views.home, name='home'),
    path('gas_station/', views.gas_station_list, name='gas_station_list'),
    path('role/', views.role_list, name='role_list'),

    path('user/', views.user_list, name='user_list'),
    path('notifications/', views.notification_list, name='notification_list'),

    path('report/', views.report_list, name='report_list'),

    path('station_rev/', views.station_rev_list, name='station_rev_list'),

    path('promotion/', views.promotion_list, name='promotion_list'),

    path('favorite_station/', views.favorite_station_list, name='favorite_station_list'),

    path('price_history/', views.price_history_list, name='price_history_list'),

    path('station_fuel/', views.station_fuel_list, name='station_fuel_list'),





]