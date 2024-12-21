from django.urls import path
from . import views


app_name = 'profil_account'

urlpatterns = [
    path('profil/', views.profile, name='profile'),

    path('add_favorite_station/', views.add_favorite_station, name='add_favorite_station'),
    path('favorite_station/', views.favorite_station, name='favorite_station'),

    path('remove_favorite_station/', views.remove_favorite_station, name='remove_favorite_station')



    ]