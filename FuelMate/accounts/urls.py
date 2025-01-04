from django.urls import path
from . import views  # Importuj widoki accounts
from stations.views import (  # Importuj widoki z aplikacji stations
    home, gas_station_list, role_list, price_history_list, favorite_station_list
)
from .views import LoginModalView, CustomLogoutView

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', LoginModalView.as_view(), name='login'),
    path('logged_in/', views.logged_in_view, name='logged_in'),
    path('logout/', CustomLogoutView.as_view(next_page='/'), name='logout'),
    # Widoki z aplikacji stations
    path('', home, name='default_page'),
    path('gas_station/', gas_station_list, name='gas_station_list'),
    path('role/', role_list, name='role_list'),
    path('price_history/', price_history_list, name='price_history_list'),
    path('favorite_station/', favorite_station_list, name='favorite_station_list'),
]
