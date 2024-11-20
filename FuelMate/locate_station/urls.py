from django.urls import path
from . import views

app_name = 'locate_station'

urlpatterns = [
    path('search/', views.logged_in_view, name='search'),
]
