# stations/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('fuel/', views.fuel_list, name='fuel_list'),
]