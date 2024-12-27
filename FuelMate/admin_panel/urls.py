from django.urls import path
from . import views
app_name = 'admin_panel'  # Zarejestrowanie przestrzeni nazw
urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete_prices/', views.delete_prices, name='delete_prices'),
    path('refresh_stations/', views.refresh_stations, name='refresh_stations'),

]
