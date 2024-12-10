from django.urls import path
from . import views


app_name = 'price_history'

urlpatterns = [
    path('list_price/', views.price_history, name='list_price'),
    path('list_price/<str:station_name>/', views.station_details, name='station_details'),



    ]